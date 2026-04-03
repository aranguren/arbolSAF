# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ArbolSAF** is a Django-based web application for CIFOR-ICRAF managing tree species data for agroforestry systems (Sistemas Agroforestales). It provides species/variable CRUD, import/export, PDF reports, and an interactive agroforestry assessment tool.

## Development Commands

```bash
# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Load initial fixture data
python manage.py loaddata ./fixtures/initial_data.json

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

## Docker Deployment

```bash
docker-compose pull
docker-compose build
docker-compose up -d
```

## Environment Variables

Database connection requires these env vars (defaults to `postgres:postgres@127.0.0.1:5432/arbolsaf`):
- `DB_NAME`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`
- `SECRET_KEY`, `DEBUG`

## Architecture

### Django App Structure
- **`core/`** — Project settings, root URLs, WSGI/ASGI entry points
- **`arbolsaf/`** — Main application with all domain logic (species, variables, references, tools)
- **`apps/authentication/`** — Login/register views
- **`apps/home/`** — UI template library and homepage routing

### Domain Model Hierarchy
```
FamilyModel → GenderModel → SpeciesModel → VariableModel
                                ↓               ↓
                         SynonymousModel   VariableTypeModel
                                          ReferenceModel
```

All models inherit from `BasicAuditModel` (abstract base with `created_by`, `modified_by`, `created`, `modified` fields).

`VariableTypeModel` supports 5 value types: `boolean`, `qualitative`, `numeric`, `range`, `text`.

### View Patterns
All views use Django class-based views (CBV) with:
- `LoginRequiredMixin` for authentication
- `GroupRequiredMixin` from `arbolsaf/permissions.py` for authorization
- Two roles: `visualizador` (viewer) and `editor` (editor); superusers bypass group checks

View modules in `arbolsaf/views/`:
- `species_views.py` — Species CRUD
- `variables_views.py` — Variable management per species
- `variable_type_views.py` — Variable type definitions
- `reference_views.py` — Citation sources
- `cross_table_views.py` — CSV export / cross-table views
- `tool_views.py` — Agroforestry assessment tool + PDF export
- `synonymous_views.py` — Species synonyms

### URL Namespace
All ArbolSAF URLs are under `/arbolsaf/` prefix (78 patterns). Key patterns use Spanish naming: `/especie/`, `/tipos_variable/`, `/referencia/`, `/tabla_cruzada/`, `/herramienta/`.

### Key Dependencies
- **`django-computedfields`** — Computed model fields (update via `python manage.py updatedata`)
- **`django-import-export`** — CSV/Excel import-export on admin and views
- **`django-wkhtmltopdf`** — Server-side PDF generation for tool reports
- **`ckeditor`** — Rich text for species descriptions
- **`django.contrib.gis`** — PostGIS geospatial support (requires PostGIS-enabled PostgreSQL)

### Static Files
Served via WhiteNoise middleware. Frontend assets in `apps/static/assets/`. No frontend build step — templates use Django template engine with inline Bootstrap and Select2.
