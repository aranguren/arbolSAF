#!/usr/bin/env bash
# =============================================================================
# restore_db.sh — Restaura un dump SQL en el entorno destino
#
# USO:
#   ./scripts/restore_db.sh <ruta_al_dump.sql> [opciones]
#
# OPCIONES:
#   --env local | dev       Entorno destino (default: local)
#   --password <pwd>        Contraseña de PostgreSQL (default: lee $PGPASSWORD)
#   --db-container <name>   Nombre del contenedor de BD (default: auto según env)
#   --web-container <name>  Nombre del contenedor web (default: auto según env)
#
# EJEMPLOS:
#   # Restaurar en local (desde carpeta Despliegue/)
#   ./scripts/restore_db.sh ../assets/clonedb20260604.sql --env local --password mysecret
#
#   # Restaurar en servidor de desarrollo (ejecutar estando en ~/src/)
#   ./scripts/restore_db.sh clonedb20260604.sql --env dev --password mysecret
# =============================================================================

set -euo pipefail

# ── Colores ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }
step()    { echo -e "\n${GREEN}══ $* ${NC}"; }

# ── Defaults ─────────────────────────────────────────────────────────────────
DUMP_FILE=""
ENV="local"
PGPWD="${PGPASSWORD:-}"
DB_USER="arbolsaf_user"
DB_NAME="arbolsaf"
DB_CONTAINER=""
WEB_CONTAINER=""

# ── Parsear argumentos ───────────────────────────────────────────────────────
if [[ $# -lt 1 ]]; then
  echo "Uso: $0 <dump.sql> [--env local|dev] [--password <pwd>] [--db-container <name>] [--web-container <name>]"
  exit 1
fi

DUMP_FILE="$1"; shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)           ENV="$2";          shift 2 ;;
    --password)      PGPWD="$2";        shift 2 ;;
    --db-user)       DB_USER="$2";      shift 2 ;;
    --db-name)       DB_NAME="$2";      shift 2 ;;
    --db-container)  DB_CONTAINER="$2"; shift 2 ;;
    --web-container) WEB_CONTAINER="$2";shift 2 ;;
    *) error "Argumento desconocido: $1" ;;
  esac
done

# ── Validaciones ─────────────────────────────────────────────────────────────
[[ -f "$DUMP_FILE" ]] || error "Dump no encontrado: $DUMP_FILE"
[[ -z "$PGPWD" ]]     && error "Falta contraseña. Usa --password <pwd> o exporta PGPASSWORD."

# Nombres de contenedores por defecto según entorno
if [[ -z "$DB_CONTAINER" ]]; then
  [[ "$ENV" == "local" ]] && DB_CONTAINER="despliegue-db-1" || DB_CONTAINER="src_db_1"
fi
if [[ -z "$WEB_CONTAINER" ]]; then
  [[ "$ENV" == "local" ]] && WEB_CONTAINER="" || WEB_CONTAINER="src_web_1"
fi

DUMP_BASENAME=$(basename "$DUMP_FILE")

warn "⚠️  Esto SOBREESCRIBE la base de datos del entorno '${ENV}'."
warn "    Dump:            $DUMP_FILE"
warn "    Contenedor BD:   $DB_CONTAINER"
read -r -p "¿Continuar? (escribe 'si' para confirmar): " CONFIRM
[[ "$CONFIRM" == "si" ]] || { info "Cancelado."; exit 0; }

# ── Asegurar que web esté corriendo para el backup ───────────────────────────
WEB_RUNNING=$(docker-compose ps --services --filter "status=running" 2>/dev/null | grep -c "^web$" || true)
if [[ "$WEB_RUNNING" -eq 0 ]]; then
  info "Iniciando web temporalmente para hacer el backup de usuarios..."
  docker-compose start web
  sleep 5
fi

# ── Paso 1: Backup de usuarios actuales ──────────────────────────────────────
step "1/8 · Guardando usuarios actuales"
docker-compose exec web python manage.py dumpdata \
  auth.user auth.group auth.permission \
  --natural-foreign --natural-primary \
  -o /code/usuarios_backup.json
info "Backup guardado en /code/usuarios_backup.json"

# ── Paso 2: Copiar dump al contenedor de BD ──────────────────────────────────
step "2/8 · Copiando dump al contenedor de BD"
docker cp "$DUMP_FILE" "${DB_CONTAINER}:/tmp/clonedb.sql"
info "Dump copiado: /tmp/clonedb.sql"

# ── Paso 3: Detener web ───────────────────────────────────────────────────────
step "3/8 · Deteniendo contenedor web"
docker-compose stop web
info "Web detenido"

# ── Paso 4: Eliminar y recrear la BD ─────────────────────────────────────────
step "4/8 · Eliminando base de datos arbolsaf"
docker-compose exec -e PGPASSWORD="$PGPWD" db \
  psql -h 127.0.0.1 -U "$DB_USER" -d postgres \
  -c "DROP DATABASE IF EXISTS ${DB_NAME};"

info "Recreando base de datos ${DB_NAME}"
docker-compose exec -e PGPASSWORD="$PGPWD" db \
  psql -h 127.0.0.1 -U "$DB_USER" -d postgres \
  -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

# ── Paso 5: Cargar el dump ────────────────────────────────────────────────────
step "5/8 · Cargando dump SQL"
docker-compose exec -e PGPASSWORD="$PGPWD" db \
  psql -h 127.0.0.1 -U "$DB_USER" -d "$DB_NAME" \
  -f /tmp/clonedb.sql
info "Dump cargado"

# ── Paso 6: Iniciar web y migraciones ────────────────────────────────────────
step "6/8 · Iniciando web y aplicando migraciones"
docker-compose start web
docker-compose exec web python manage.py migrate
info "Migraciones aplicadas"

# ── Paso 7: Restaurar solo usuarios locales que no existen en el dump ────────
step "7/8 · Restaurando usuarios exclusivos del entorno '${ENV}'"

# Obtener usernames que ya existen en la BD (vinieron del dump)
EXISTING_USERS=$(docker-compose exec -T web python manage.py shell -c \
  "from django.contrib.auth import get_user_model; U=get_user_model(); print(','.join(U.objects.values_list('username',flat=True)))" \
  2>/dev/null | tr -d '\r')

info "Usuarios en el dump: $EXISTING_USERS"

# Filtrar el backup: solo cargar usuarios cuyo username NO está ya en la BD
docker-compose exec -T web python manage.py shell << PYEOF
import json, os
from django.contrib.auth import get_user_model

existing = set(get_user_model().objects.values_list('username', flat=True))

with open('/code/usuarios_backup.json') as f:
    data = json.load(f)

# Separar auth.user (filtrar por username) del resto (grupos, permisos — siempre cargar)
users_to_add = [
    obj for obj in data
    if obj['model'] == 'auth.user' and obj['fields']['username'] not in existing
]
other_objects = [obj for obj in data if obj['model'] != 'auth.user']

filtered = other_objects + users_to_add

with open('/code/usuarios_nuevos.json', 'w') as f:
    json.dump(filtered, f)

print(f"Usuarios en backup: {len([o for o in data if o['model']=='auth.user'])}")
print(f"Usuarios a agregar (no están en dump): {len(users_to_add)}")
PYEOF

docker-compose exec web python manage.py loaddata /code/usuarios_nuevos.json
info "Usuarios exclusivos del entorno restaurados (los del dump no fueron sobreescritos)"

# ── Paso 8: Estáticos y restart ───────────────────────────────────────────────
step "8/8 · Colectando estáticos y reiniciando"
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart web

echo -e "\n${GREEN}✓ Restauración completada exitosamente.${NC}"
