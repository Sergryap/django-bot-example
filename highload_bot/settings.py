"""
Django settings for highload_bot project.

Generated by 'django-admin startproject' using Django 1.11.21.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import rollbar
from environs import Env


env = Env()
env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', default='empty')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', '45.84.226.238', 'localhost', '[::1]'])


# Application definition

INSTALLED_APPS = [
    'admin_shortcuts',  # should be just before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'import_export',
    'rest_framework',
    'storages',
    'debug_toolbar',

    'telegram_bot.apps.TelegramBotConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # above all other middleware apart from SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', # recommended before CsrfViewMiddleware
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'highload_bot.middleware.RollbarNotifierMiddlewareExcluding404AndPermissionDenied',  # should be listed last
]

ROOT_URLCONF = 'highload_bot.urls'

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

WSGI_APPLICATION = 'highload_bot.wsgi.application'

_default_sqlite_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {"default": env.dj_db_url('DATABASE_URL', _default_sqlite_url)}

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


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


AWS_ACCESS_KEY_ID = env.str('S3_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = env.str('S3_SECRET_ACCESS_KEY', None)

AWS_S3_REGION_NAME = env.str('S3_REGION_NAME', 'fra1')
AWS_S3_ENDPOINT_URL = env.str('S3_ENDPOINT_URL', f'https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com')
AWS_STORAGE_BUCKET_NAME = env.str('STORAGE_BUCKET_NAME', 'levelupbots')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = env.str('S3_MEDIA_LOCATION', 'highload-bots-media')

MEDIA_URL = env.str('MEDIA_URL', default='/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if AWS_ACCESS_KEY_ID:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

ROLLBAR = {
    'access_token': env.str('ROLLBAR_TOKEN', default=''),
    'environment': env.str('ROLLBAR_ENVIRONMENT', default='development'),
    'branch': 'master',
    'root': BASE_DIR,
    'enabled': bool(env.str('ROLLBAR_TOKEN', default='')),
    'locals': {
        'enabled': True,
        'safe_repr': False,  # enable repr(obj)
    }
}
rollbar.init(**ROLLBAR)

TELEGRAM_ACCESS_TOKEN = env.str('TELEGRAM_ACCESS_TOKEN')

ADMIN_SHORTCUTS = [
    {
        'title': 'Ребус',
        'shortcuts': [
            {
                'title': 'Добавить Ребус',
                'url_name': 'admin:telegram_bot_rebus_add',
            },
        ]
    },
    {
        'title': 'Розыгрыши',
        'shortcuts': [
            {
                'title': 'Настройка розыгрышей',
                'url_name': 'admin:telegram_bot_draw_changelist',
            },
        ],
    },
    {
        'title': 'Опросы',
        'shortcuts': [
            {
                'title': 'Скачать результат опросов',
                'url': '/poll/file.csv',
            },
        ],
    }

]

INTERNAL_IPS = env.str('INTERNAL_IPS', '127.0.0.1')  # for django debug_toolbar
