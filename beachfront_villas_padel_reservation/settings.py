"""
Django settings for beachfront_villas_padel_reservation project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import Config, RepositoryEnv
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

# Get the DJANGO_ENV value
django_env = os.getenv('DJANGO_ENV', 'local')  # Default to 'local' if not set

# Set the path for the appropriate .env file based on DJANGO_ENV
env_file = '.env'

# Initialize Config with the selected .env file
config = Config(RepositoryEnv(os.path.join(BASE_DIR, env_file)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')  # Use a default for local dev


# SECURITY WARNING: don't run with debug turned on in production!
if django_env == 'local':
    DEBUG = True
else:
    DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = config("ALLOWED_HOSTS", "*").split(",")

if django_env == 'production':
    CSRF_TRUSTED_ORIGINS = [
        'https://beachfront-padel-reservation.up.railway.app',
        'http://beachfront-padel-reservation.up.railway.app',  # Add if using http
    ]

    CORS_ALLOWED_ORIGINS = [
        'https://beachfront-padel-reservation.up.railway.app',
    ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'home'
]

MIDDLEWARE = []

if django_env == 'production':
    MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'beachfront_villas_padel_reservation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'beachfront_villas_padel_reservation.wsgi.application'


# Database
if django_env == 'local':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:  # Production (PostgreSQL)
    DATABASES = {
        'default': dj_database_url.config(default=config('DATABASE_URL'))
    }

# DATABASE_URL = os.environ.get('DATABASE_URL')


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# User Model Path
AUTH_USER_MODEL = 'home.CustomUser'

# custom login URL
LOGIN_URL = '/login/'

# URL to redirect to after successful login
LOGIN_REDIRECT_URL = '/'


# Session Settings
SESSION_COOKIE_AGE = 3600  # Session ends when the browser is closed after 1 hour in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory where collectstatic collects files

if django_env == 'production':
    # STATICFILES_DIRS is not necessary in production unless you have additional directories
    STATICFILES_DIRS = []  # Ensure this is an empty list or omit it altogether

    # Compress static files for performance
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (for user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
