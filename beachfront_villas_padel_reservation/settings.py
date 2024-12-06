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


# Check for the environment (default to 'production')
# ENVIRONMENT = os.getenv('DJANGO_ENV', 'production')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

# Get the DJANGO_ENV value
django_env = os.getenv('DJANGO_ENV', 'local')  # Default to 'local' if not set

# Set the path for the appropriate .env file based on DJANGO_ENV
env_file = '.env'

# Initialize Config with the selected .env file
# config = Config(search_path=os.path.dirname(__file__), env_file=env_file)
config = Config(RepositoryEnv(os.path.join(BASE_DIR, env_file)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-y33pg40a1)+70$e%g!5ahy6^&gh-#l($0j^gq4va=f32$0lx*#'
SECRET_KEY = config('DJANGO_SECRET_KEY')  # Use a default for local dev


# SECURITY WARNING: don't run with debug turned on in production!
if django_env == 'local':
    DEBUG = True
else:
    DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = config("ALLOWED_HOSTS", "*").split(",")
print("ALLOWED_HOSTS:", ALLOWED_HOSTS)

CSRF_TRUSTED_ORIGINS = [
    'https://beachfront-padel-reservation.up.railway.app',
    'http://beachfront-padel-reservation.up.railway.app',  # Add if using http
]

CORS_ALLOWED_ORIGINS = [
    'https://beachfront-padel-reservation.up.railway.app',
]

# test

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home'
]

MIDDLEWARE = [
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
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres.upgzsgbjaacpxvvcasxr',
#         'PASSWORD': 'Storm@151994#',
#         'HOST': 'aws-0-eu-west-2.pooler.supabase.com',
#         'PORT': '6543',  # usually 5432
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': os.getenv('POSTGRES_HOST'),
#         'PORT': os.getenv('POSTGRES_PORT'),
#     }
# }

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
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': config('POSTGRES_DB'),
    #         'USER': config('POSTGRES_USER'),
    #         'PASSWORD': config('POSTGRES_PASSWORD'),
    #         'HOST': config('POSTGRES_HOST'),
    #         'PORT': config('POSTGRES_PORT'),
    #     }
    # }

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



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory where static files are collected

# Media files (for user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
