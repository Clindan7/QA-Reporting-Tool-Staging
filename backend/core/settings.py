import os
from pathlib import Path

from corsheaders.defaults import default_headers
import django
from django.utils.log import DEFAULT_LOGGING
from dotenv import load_dotenv
import logging.config

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    'rest_framework',
    'rest_framework_simplejwt',
    'users',
    'project',
    'report'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'util.middleware.RefererMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'core.urls'

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
                'django.contrib.messages.context_processors.messages'
              
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

ENV = os.environ.get("ENV")

LOGLEVEL = os.environ.get("ENV_LOG_LEVEL", "info").upper()
DJANGO_SERVER = "django.server"

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
        DJANGO_SERVER: DEFAULT_LOGGING["formatters"][DJANGO_SERVER],
    },
    "handlers": {
        "file": {
            "level": LOGLEVEL,
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join(BASE_DIR, "application.log"),
        },
        "console": {
            "level": LOGLEVEL,
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        DJANGO_SERVER: DEFAULT_LOGGING["handlers"][DJANGO_SERVER],
    },
    "loggers": {
        "": {
            "level": LOGLEVEL,
            "handlers": ["file", "console"],
        },
        "app": {
            "level": LOGLEVEL,
            "handlers": ["file", "console"],
            "propagate": False,
        },
        DJANGO_SERVER: DEFAULT_LOGGING["loggers"][DJANGO_SERVER],
        "django.request": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
})

CORS_ALLOW_HEADERS = list(default_headers)

ENABLE_CORS = os.getenv("ENV_ENABLE_CORS", "false")

if ENABLE_CORS == "true":
    ALLOWED_DOMAINS = os.getenv("ENV_CORS_ALLOWED").split(",")
    CORS_ORIGIN_WHITELIST = ALLOWED_DOMAINS
    CORS_ALLOW_HEADERS += ("access-control-allow-origin",)
    CORS_ALLOW_CREDENTIALS = True
else:
    # Same as allow ["*"], CORS_ORIGIN_WHITELIST = ["*"] is not allowed
    CORS_ALLOW_ALL_ORIGINS = True

ENABLE_CORS = os.environ.get("ENV_ENABLE_CORS", "false")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ENV_CORE_URL_CUSTOMER = os.environ.get("ENV_CORE_URL_CUSTOMER")

ENV_CORE_URL_TICKET = os.environ.get("ENV_CORE_URL_TICKET")
