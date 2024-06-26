"""
Django settings for persacc project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import environ
from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-9^&z#**ky(m+z@_32vac#&x0ex=h(x5%!^q+gp&yf7fp970%d-'
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = env.bool('DEBUG', default=False)

# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'catalog.apps.catalogConfig',
    'user.apps.userConfig',
    'price.apps.PriceConfig',
    'django_filters',
    'document.apps.documentConfig',
    'django_celery_beat',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'persacc.urls'

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

WSGI_APPLICATION = 'persacc.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DB_DEFAULT = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}
DB_ENGINE = env.str('DB_ENGINE', default='django.db.backends.sqlite3')

DATABASES = {
    'default': env.db(
        'DB_URL',
        engine=DB_ENGINE,
        default=os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'EXCEPTION_HANDLER': 'persacc.exceptions.custom_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
}

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
     "http://localhost",
     "http://localhost:",
     "http://localhost:3000",
     "https://localhost:3000",
     "https://localhost",
     "https://localhost:",
 ]

#CORS_ALLOWED_ORIGINS = env.list(
#    'CORS_ALLOWED_ORIGINS',
#    default=[
#        "http://localhost:",
#        "http://localhost:3000",
#    ]
#)

CSRF_COOKIE_NAME = "XSRF-TOKEN"
CORS_ALLOW_HEADERS = list(default_headers) + ["x-xsrf-token",]
#CORS_ORIGIN_ALLOW_ALL = False

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    #"ROTATE_REFRESH_TOKENS": True,
    #"BLACKLIST_AFTER_ROTATION": True,
    #"UPDATE_LAST_LOGIN": False,
    #"TOKEN_OBTAIN_SERIALIZER": "user.serializers.TokenObtainLifetimeSerializer",
    #"TOKEN_REFRESH_SERIALIZER": "user.serializers.TokenRefreshLifetimeSerializer",
}

EMAIL_CONFIG = env.email_url('EMAIL_CONFIG')
vars().update(EMAIL_CONFIG)

HTTP_SERVICE = env.str('HTTP_SERVICE')
HTTP_USER = env.str('HTTP_USER')
HTTP_PASSWORD = env.str('HTTP_PASSWORD')

CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')

# CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')


    
