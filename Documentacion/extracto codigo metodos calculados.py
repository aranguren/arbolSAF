# EXTRACTO DE CÓDIGO — CÁLCULO DE VALORES PARA LAS CATEGORÍAS
# Archivo fuente: arbolsaf/models.py (clase SpeciesModel)
# Actualizado: junio 2026
#
# CAMBIOS RESPECTO A LA VERSIÓN ANTERIOR:
#   - Se añadieron helpers _any_bool() y _qual_options() que reemplazan
#     los bloques repetitivos de lookup por variable.
#   - valor_madera: nuevas variables (v169, v147, v163, v167, v168); exclusión
#     por v104 (palmera/herbacea) usando _qual_options.
#   - valor_fruta: escala escalonada con v170 (alto), v130 (medio), v23 (bajo).
#   - valor_otros_usos: lógica de grupos ponderados (alto/medio/bajo), resultado Float.
#   - valor_biodiversidad: incluye nativa, endémica, IUCN cualitativo (v56),
#     CITES (v59) y fauna (v89, v90, v18, v91, v177, v176), normalizado a 0–6.
#   - valor_suelo: variables actualizadas (v116, v171, v37, v95, v161, v115),
#     normalizado a escala 0–3.
#   - valor_microclima: eliminado del cálculo del IVIM.
#   - ivim: suma directa de los 5 valores (sin índices intermedios).
#   - indice_multiuso e indice_valor_uso_relativo: eliminados.


# ── Helpers ──────────────────────────────────────────────────────────────────

def _any_bool(self, cod):
    """True si alguna fila VariableModel(cod_var=cod) tiene valor_boolean=True."""
    return self.variables.filter(
        tipo_variable__cod_var__iexact=cod,
        valor_boolean=True,
    ).exists()

def _qual_options(self, cod):
    """Conjunto de nombres de opciones cualitativas (lowercase, stripped)
    unidos de TODAS las filas VariableModel(cod_var=cod) de la especie."""
    nombres = self.variables.filter(
        tipo_variable__cod_var__iexact=cod,
    ).values_list('valores_cualitativos__nombre', flat=True)
    return {n.lower().strip() for n in nombres if n}


# ── Campos computados — valores numéricos ────────────────────────────────────

@computed(models.IntegerField(_("Valor para  Madera"), default=0), depends=[])
def valor_madera(self):
    # Palmeras y herbáceas (v104) no tienen valor maderable
    if self._qual_options('v104') & {'palmera', 'herbacea'}:
        return 0
    if len(self.get_variables) == 0:
        return 0

    v169 = self._any_bool('v169')  # madera valiosa / uso maderable reconocido
    v147 = self._any_bool('v147')  # especie maderera de alto valor

    if v169 and v147:
        return 3
    if v169:
        return 2
    if self._any_bool('v163') or self._any_bool('v167') or self._any_bool('v168'):
        return 1
    return 0


@computed(models.IntegerField(_("Valor para  Fruta"), default=0), depends=[])
def valor_fruta(self):
    if len(self.get_variables) == 0:
        return 0

    if self._any_bool('v170'):   # fruto comercialmente valorado
        return 3
    if self._any_bool('v130'):   # fruto comestible con potencial
        return 2
    if self._any_bool('v23'):    # fruto comestible básico
        return 1
    return 0


@computed(models.FloatField(_("Valor para Otros usos"), default=0.0), depends=[])
def valor_otros_usos(self):
    if len(self.get_variables) == 0:
        return 0.0

    # Grupo alto: leña, carbón, forraje
    alto  = 3 if any(self._any_bool(c) for c in ('v162', 'v142', 'v39')) else 0
    # Grupo medio: medicinal, artesanías
    medio = 2 if any(self._any_bool(c) for c in ('v113', 'v111')) else 0
    # Grupo bajo: tintes-pigmentos, cosméticos/repelentes, fibra
    bajo  = 1 if any(self._any_bool(c) for c in ('v102', 'v112', 'v70')) else 0

    return round((alto + medio + bajo) / 2.0, 2)   # escala 0–3


@computed(models.FloatField(_("Valor para Biodiversidad"), default=0.0), depends=[])
def valor_biodiversidad(self):
    if len(self.get_variables) == 0:
        return 0.0

    nativa = 1.0 if self.nativa else 0.0

    # v56 IUCN (cualitativa): EN=1, VU=0.5, NT=0.25 — agrega TODAS las filas
    nombres_v56 = self._qual_options('v56')
    if   'en' in nombres_v56: v56 = 1.0
    elif 'vu' in nombres_v56: v56 = 0.5
    elif 'nt' in nombres_v56: v56 = 0.25
    else:                      v56 = 0.0

    # v59 CITES (cualitativa): Apéndice II = 1
    v59 = 1.0 if 'ii' in self._qual_options('v59') else 0.0

    def _b(cod): return 1.0 if self._any_bool(cod) else 0.0

    v64  = _b('v64')   # endémica del Perú
    v89  = _b('v89')   # recurso para aves
    v90  = _b('v90')   # recurso para micromamíferos
    v18  = _b('v18')   # recurso para abejas
    v91  = _b('v91')   # recurso para murciélagos
    v177 = _b('v177')  # recurso para primates
    v176 = _b('v176')  # recurso para mamíferos mayores

    suma = nativa + v56 + v59 + v64 + v89 + v90 + v18 + v91 + v177 + v176
    return round(suma * 6.0 / 10.0, 2)   # normalizado a escala 0–6


@computed(models.FloatField(_("Valor para el Suelo"), default=0.0), depends=[])
def valor_suelo(self):
    if len(self.get_variables) == 0:
        return 0.0

    v116 = 1 if self._any_bool('v116') else 0   # mejora estructura del suelo
    v171 = 1 if self._any_bool('v171') else 0   # presencia de nódulos

    # v37 fenología foliar (cualitativa): caducifolio=2, semicaducifolio=1
    nombres_v37 = self._qual_options('v37')
    if   'caducifolio'      in nombres_v37: v37 = 2
    elif 'semicaducifolio'  in nombres_v37: v37 = 1
    else:                                    v37 = 0

    # v95 aporta fertilidad (cualitativa)
    nombres_v95 = self._qual_options('v95')
    v95 = 1 if any(n in nombres_v95 for n in (
        'fertilidad del suelo', 'recuperacion de suelos', 'recuperacion de suelo'
    )) else 0

    # v161 tolerancia a estrés hídrico (cualitativa)
    nombres_v161 = self._qual_options('v161')
    v161 = 1 if ('sequia' in nombres_v161 or 'sequía' in nombres_v161) else 0

    # v115 asociación microbiana (cualitativa): bacterias o micorrizas
    nombres_v115 = self._qual_options('v115')
    v115 = 1 if any(n in nombres_v115 for n in ('bacterias', 'micorrizas')) else 0

    # puntaje bruto máx = 7 (v37 puede valer 2), normalizado a 0–3
    puntaje_bruto = v116 + v171 + v37 + v95 + v161 + v115
    return round(puntaje_bruto * 3.0 / 7.0, 2)


# ── IVIM ─────────────────────────────────────────────────────────────────────
# Escala 0–18: suma directa de los 5 valores (madera 0-3, fruta 0-3,
# otros_usos 0-3, biodiversidad 0-6, suelo 0-3).
# Nota: valor_microclima fue eliminado del IVIM en la versión actual.

@computed(models.FloatField(_("IVIM"), default=0.0),
          depends=[('self', ['valor_madera', 'valor_fruta', 'valor_otros_usos',
                             'valor_biodiversidad', 'valor_suelo'])])
def ivim(self):
    return round(
        self.valor_madera + self.valor_fruta + self.valor_otros_usos +
        self.valor_biodiversidad + self.valor_suelo, 2
    )


# ── Campos de categoría (texto) ───────────────────────────────────────────────
# Cada campo numérico tiene su equivalente de texto para facilitar filtros en admin.

@computed(models.CharField(_("Valor para Madera"), max_length=50,
                            choices=VALUES_CHOICES, default='ninguno'),
          depends=[('self', ['valor_madera'])])
def valor_madera_category(self):
    if   self.valor_madera == 0: return 'ninguno'
    elif self.valor_madera == 1: return 'bajo'
    elif self.valor_madera == 2: return 'medio'
    else:                        return 'alto'


@computed(models.CharField(_("Valor para Fruta"), max_length=50,
                            choices=VALUES_CHOICES, default='ninguno'),
          depends=[('self', ['valor_fruta'])])
def valor_fruta_category(self):
    if   self.valor_fruta == 0: return 'ninguno'
    elif self.valor_fruta == 1: return 'bajo'
    elif self.valor_fruta == 2: return 'medio'
    else:                       return 'alto'


@computed(models.CharField(_("Valor para otros Usos"), max_length=50,
                            choices=VALUES_CHOICES, default='ninguno'),
          depends=[('self', ['valor_otros_usos'])])
def valor_otros_usos_category(self):
    if   self.valor_otros_usos == 0: return 'ninguno'
    elif self.valor_otros_usos <= 1: return 'bajo'
    elif self.valor_otros_usos <= 2: return 'medio'
    else:                            return 'alto'


@computed(models.CharField(_("Valor para Biodiversidad"), max_length=50,
                            choices=VALUES_CHOICES, default='ninguno'),
          depends=[('self', ['valor_biodiversidad'])])
def valor_biodiversidad_category(self):
    if   self.valor_biodiversidad == 0: return 'ninguno'
    elif self.valor_biodiversidad <= 2: return 'bajo'
    elif self.valor_biodiversidad <= 4: return 'medio'
    else:                               return 'alto'


@computed(models.CharField(_("Valor para Suelo"), max_length=50,
                            choices=VALUES_CHOICES, default='ninguno'),
          depends=[('self', ['valor_suelo'])])
def valor_suelo_category(self):
    if   self.valor_suelo == 0: return 'ninguno'
    elif self.valor_suelo <= 1: return 'bajo'
    elif self.valor_suelo <= 2: return 'medio'
    else:                       return 'alto'
