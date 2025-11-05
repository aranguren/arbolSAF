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
# Never use a default SECRET_KEY in production - this will raise an error if not set
SECRET_KEY = config('SECRET_KEY', default='')
if not SECRET_KEY or SECRET_KEY == 'S#perS3crEt_1122':
    if config('DEBUG', default=False, cast=bool):
        # Development fallback only
        SECRET_KEY = 'dev-secret-key-change-in-production'
    else:
        raise ValueError("SECRET_KEY must be set in environment variables for production")

# SECURITY WARNING: don't run with debug turned on in production!
# Default is False for security - must explicitly enable for development
DEBUG = config('DEBUG', default=False, cast=bool)

# load production server from .env
# Validate SERVER configuration to prevent Host header injection
SERVER = config('SERVER', default='127.0.0.1')
ALLOWED_HOSTS_LIST = ['localhost', '127.0.0.1']

# Whitelist of allowed production domains
ALLOWED_PRODUCTION_HOSTS = [
    'arbolsaf.denebinc.com',
]

# Add SERVER if it's in the whitelist or if DEBUG is True
if DEBUG or SERVER in ALLOWED_PRODUCTION_HOSTS + ['127.0.0.1', 'localhost']:
    if SERVER not in ALLOWED_HOSTS_LIST:
        ALLOWED_HOSTS_LIST.append(SERVER)
else:
    # In production with unknown host, fail safe
    import sys
    print(f"WARNING: SERVER '{SERVER}' is not in the whitelist of allowed hosts", file=sys.stderr)
    if not DEBUG:
        print("ERROR: Cannot start in production mode with unrecognized host", file=sys.stderr)

ALLOWED_HOSTS = ALLOWED_HOSTS_LIST

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
    'arbolsaf', 
    'apps.home'  # Enable the inner home (home)
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
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "/arbolsaf/especie/listado"  # Route defined in home/urls.py
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

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################

MEDIA_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MEDIA_ROOT = os.path.join(MEDIA_BASE_DIR, 'media')
MEDIA_URL = '/uploaded/'


#############################################################
# SECURITY SETTINGS
#############################################################

# Browser security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS and SSL settings (enable in production)
# Uncomment these when deploying with HTTPS
# SECURE_SSL_REDIRECT = not DEBUG  # Redirect HTTP to HTTPS in production
# SESSION_COOKIE_SECURE = not DEBUG  # Send session cookie only over HTTPS
# CSRF_COOKIE_SECURE = not DEBUG  # Send CSRF cookie only over HTTPS
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Session and Cookie Security
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_COOKIE_AGE = 3600  # 1 hour session timeout

# CSRF Cookie Security
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF token
CSRF_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# File Upload Security
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000  # Prevent DoS via large number of fields
