# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
ALLOWED_HOSTS = ['localhost', '127.0.0.1','20.112.116.172','arbolsaf.cifor-icraf.org', config('SERVER', default='127.0.0.1')]
CSRF_TRUSTED_ORIGINS = [
    "https://arbolsaf-dev.cifor-icraf.org", # Not mandatory but sometimes it hits a CSRF error in POST
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'computedfields',
    'import_export',
    'ckeditor',
    'ckeditor_uploader',
    'arbolsaf',
    'apps.home',  # Enable the inner home (home)
    'django_browser_reload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_URL          = "/login/"                          # URL real del login
LOGIN_REDIRECT_URL = "/arbolsaf/especie/listado"  # Entrada plataforma de datos tras login
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'arbolsaf.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'arbolsaf'), #arbolsaf8 arbolsaf_smart
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': int(os.getenv('DB_PORT', 5432)),
        'USER': os.getenv('DB_USER','postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD','postgres')
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Cache-busting: appends content hash to filenames served via {% static %}.
# Hardcoded /static/... paths still work (original files are preserved).
# Requires: docker-compose exec web python manage.py collectstatic --noinput
STATICFILES_STORAGE = 'core.storage.CompressedManifestStorage'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################

MEDIA_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MEDIA_ROOT = os.path.join(MEDIA_BASE_DIR, 'media')
MEDIA_URL = '/uploaded/'

# Subcarpeta dentro de MEDIA_ROOT donde CKEditor sube las imágenes del editor
CKEDITOR_UPLOAD_PATH = 'editor_uploads/'
# Solo admins pueden subir — no requiere autenticación adicional
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_BROWSE_SHOW_DIRS = True

# ── CKEditor ─────────────────────────────────────────────────────────
# allowedContent=True: no eliminar clases, atributos ni estilos inline
# contentsCss: carga el CSS de la herramienta para que los títulos y
#   subtítulos se vean con el estilo correcto dentro del editor
CKEDITOR_CONFIGS = {
    'default': {
        # No eliminar clases HTML ni atributos personalizados
        'allowedContent': True,
        'extraAllowedContent': '*(*)[*]{*}',
        # CSS dedicado para el iframe del editor (sin selectores .tool-page/.arbol-main)
        'contentsCss': ['/static/assets/css/herramienta/ckeditor-content.css'],
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['Image', 'Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
        ],
    }
}
