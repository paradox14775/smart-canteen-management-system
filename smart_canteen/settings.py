
"""
Django settings for smart_canteen project.
Smart Canteen Management System (SCMS) - IPU MCA 269 Minor Project
"""

import os
from pathlib import Path

import pymysql
import dj_database_url

# Install PyMySQL as MySQLdb driver
pymysql.install_as_MySQLdb()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# SECURITY SETTINGS
# --------------------------------------------------

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-local-development-only-key'
)

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in (
    'true', '1', 'yes'
)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        'DJANGO_ALLOWED_HOSTS',
        'localhost,127.0.0.1'
    ).split(',')
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'DJANGO_CSRF_TRUSTED_ORIGINS', ''
    ).split(',')
    if origin.strip()
]

# Render provides this hostname automatically for deployed web services.
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(
        f'https://{RENDER_EXTERNAL_HOSTNAME}'
    )

# Render terminates HTTPS at its proxy.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600

# Render HTTPS proxy support
SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO', 'https'
)


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

AUTH_USER_MODEL = 'accounts.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party applications
    'rest_framework',

    # Local applications
    'apps.accounts',
    'apps.menu',
    'apps.orders',
    'apps.inventory',
    'apps.analytics',
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

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


# --------------------------------------------------
# URL AND TEMPLATE CONFIGURATION
# --------------------------------------------------

ROOT_URLCONF = 'smart_canteen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'smart_canteen.wsgi.application'


# --------------------------------------------------
# DATABASE CONFIGURATION
# PostgreSQL (Render) / SQLite (Local) / MySQL
# --------------------------------------------------

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Production PostgreSQL database
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }

else:
    USE_SQLITE = os.getenv(
        'USE_SQLITE', 'True'
    ).lower() in ('true', '1', 'yes')

    if USE_SQLITE:
        # Local development database
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

    else:
        # MySQL database
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.getenv(
                    'DB_NAME', 'smart_canteen_db'
                ),
                'USER': os.getenv('DB_USER', 'root'),
                'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
                'HOST': os.getenv('DB_HOST', 'localhost'),
                'PORT': os.getenv('DB_PORT', '3306'),
                'OPTIONS': {
                    'charset': 'utf8mb4',
                    'init_command': (
                        "SET sql_mode='STRICT_TRANS_TABLES'"
                    ),
                }
            }
        }


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------

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


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# --------------------------------------------------
# STATIC FILE CONFIGURATION
# WhiteNoise for Render deployment
# --------------------------------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


# --------------------------------------------------
# MEDIA FILE CONFIGURATION
# --------------------------------------------------

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# --------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------------------------------------------------
# AUTHENTICATION ROUTING
# --------------------------------------------------

LOGIN_URL = 'accounts:login'

LOGIN_REDIRECT_URL = 'accounts:dashboard'

LOGOUT_REDIRECT_URL = 'accounts:login'
