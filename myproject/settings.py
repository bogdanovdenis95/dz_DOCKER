
from pathlib import Path
import os
import environ
from datetime import timedelta
import stripe
from celery.schedules import crontab


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-#g+24!*yh@0l6skj2!_u(=pbtaob(=yyb)4x)0vv&fs&=7f!_e"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

STRIPE_TEST_SECRET_KEY = 'sk_test_51Pq255AxQcSK7FmoDMwhvLtEfpZBS0yDCVzo5rfbPhObsYAWzvYeM8xaf9iCh5BNp3mw2Ib0N0Rbw4c3SogQX6Ev00MJdZzUC0'
STRIPE_TEST_PUBLIC_KEY =  'pk_test_51Pq255AxQcSK7Fmo5pDvxR5ks7MilzdDibWgKLHLZorigB6atypcWNv4QERLxtPF0AtkXDNxsgqS4PRYcZ1qyMC700pL971Qbn'

stripe.api_key = STRIPE_TEST_SECRET_KEY

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myproject",
    "rest_framework",
    "users",
    "lms",
    "django_filters",
    "rest_framework_simplejwt",
    "drf_yasg",
    "django_celery_beat",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "myproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'skypro',
        'USER': 'postgres',
        'PASSWORD': 'skypro',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'users.User'


REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULE = {
    'deactivate-inactive-users-every-day': {
        'task': 'users.tasks.deactivate_inactive_users',
        'schedule': crontab(hour=0, minute=0),  # Выполнять каждый день в полночь
    },
}

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'bogdanovskypro@yandex.ru'
EMAIL_HOST_PASSWORD = 'fpkieozmdqcxlsgp'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER