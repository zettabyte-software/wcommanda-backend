import datetime
import logging
import os
import pathlib
import warnings

from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

import stripe
from corsheaders.defaults import default_headers

from utils.env import get_bool_from_env, get_env_var

stripe.api_key = get_env_var("STRIPE_SECRET_KEY")

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

SECRET_KEY = get_env_var("DJANGO_SECRET_KEY")

DEBUG = get_bool_from_env("DJANGO_DEBUG", True)

MODE = get_env_var("DJANGO_MODE")

IN_DEVELOPMENT = MODE == "development"

IN_PRODUCTION = MODE == "production"

EXECUTION = get_env_var("DJANGO_EXECUTION_MODE")


if not SECRET_KEY and DEBUG:
    warnings.warn("'SECRET_KEY' não foi configurada, using a random temporary key.", stacklevel=2)
    SECRET_KEY = get_random_secret_key()

if IN_PRODUCTION:
    import sentry_sdk

    sentry_sdk.init(
        dsn=get_env_var("SENTRY_DSN"),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


ALLOWED_HOSTS = [
    # dev
    "127.0.0.1",
    "localhost",
    "191.101.234.208",
    # prod
    ".wcommanda.com.br",
]

CSRF_TRUSTED_ORIGINS = [
    # devlopment
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    # production
    "https://*.wcommanda.com.br",
]


SITE_ID = 1

ADMINS = [("Davi Silva Rafacho", "davi.s.rafacho@gmail.com")]

MANAGERS = ADMINS


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

LIBS_APPS = [
    "auditlog",
    "cachalot",
    "corsheaders",
    "django_multitenant",
    "django_filters",
    "rest_framework",
]

WCOMMANDA_APPS = [
    # business
    "apps.clientes",
    "apps.comandas",
    "apps.descontos",
    "apps.estoque",
    "apps.fidelidade",
    "apps.filas",
    "apps.filiais",
    "apps.financeiro",
    "apps.garcons",
    "apps.ifood",
    "apps.mesas",
    "apps.notificacoes",
    "apps.pedidos",
    "apps.produtos",
    "apps.reservas",
    "apps.users",
    "apps.vendas",
    # system
    "apps.system.assinaturas",
    "apps.system.autenticacao",
    "apps.system.base",
    "apps.system.core",
    "apps.system.conf",
]

INSTALLED_APPS = DJANGO_APPS + LIBS_APPS + WCOMMANDA_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "threadlocals.middleware.ThreadLocalMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "apps.system.assinaturas.middleware.AssinaturaMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
]


ROOT_URLCONF = "api.urls"


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
            ],
        },
    },
]


WSGI_APPLICATION = "api.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": get_env_var("DATABASE_HOST"),
        "NAME": get_env_var("DATABASE_NAME"),
        "USER": get_env_var("DATABASE_USER"),
        "PASSWORD": get_env_var("DATABASE_PASSWORD"),
        "PORT": get_env_var("DATABASE_PORT"),
        "CONN_MAX_AGE": 60 * 60 * 3,
    },
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{get_env_var('REDIS_HOST')}:{get_env_var('REDIS_PORT')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


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

AUTH_USER_MODEL = "users.Usuario"


DATE_FORMAT = "d/m/Y"

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_TZ = True

USE_I18N = True

LANGUAGES = [
    ("pt-br", _("Português (Brasil)")),
    ("en", _("Inglês")),
    ("es", _("Espanhol")),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]


STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_USE_TLS = True

EMAIL_HOST = "smtp.hostinger.com"

EMAIL_HOST_USER = "nao-responda@wcommanda.com.br"

EMAIL_HOST_PASSWORD = get_env_var("EMAIL_PASSWORD")

EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = "nao-responda@wcommanda.com.br"


LOGGING_ROOT = os.path.join(BASE_DIR, "logs/")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "api_formatter": {
            "format": "[%(asctime)s] %(name)s [%(levelname)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "cloud_formatter": {
            "format": "[%(asctime)s] wcommanda %(name)s: [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "filters": {
        "warnings_filter": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno == logging.WARNING,
        },
        "api_filter": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno >= logging.INFO,
        },
        "error_filter": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno >= logging.ERROR,
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "api_formatter",
        },
        "api_activity": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "api_activity.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 10,
            "formatter": "api_formatter",
            "filters": ["api_filter"],
        },
        "api_warnings": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "warnings.log"),
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 2,
            "formatter": "api_formatter",
            "filters": ["warnings_filter"],
        },
        "api_errors": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "errors.log"),
            "maxBytes": 1024 * 1024 * 50,
            "backupCount": 10,
            "formatter": "api_formatter",
            "filters": ["error_filter"],
        },
        "api_errors_mail": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "api_formatter",
            "filters": ["error_filter"],
        },
        "api_cloud_log": {
            "level": "DEBUG",
            "class": "logging.handlers.SysLogHandler",
            "formatter": "cloud_formatter",
            "address": ("logs.papertrailapp.com", 17562),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "pika": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "httpx": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "httpcore": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "botocore": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "urllib3": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "twilio": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "django_lifecycle": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "api_activity", "api_errors"],
        "level": "INFO",
        "propagate": True,
        "formatter": "simple",
    },
}

if IN_PRODUCTION:
    LOGGING["root"]["handlers"] += ["api_cloud_log", "api_errors_mail"]


# wcommanda
AUTH_QUERY_PARAM_NAME = "jwt"

TENANT_HOST_HEADER = "X-Wcommanda-Host"


# corsheaders
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + [TENANT_HOST_HEADER]


# rest framework
REST_FRAMEWORK = {
    "PAGE_SIZE": 30,
    "DEFAULT_PAGINATION_CLASS": "apps.system.core.pagination.CustomPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.system.core.authentications.JWTAuthentication",
        "apps.system.core.authentications.JWTQueryParamAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
}

# drf simple jwt
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ["Bearer"],
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=365 if IN_DEVELOPMENT else 1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=365 if IN_DEVELOPMENT else 3),
    "TOKEN_OBTAIN_SERIALIZER": "apps.system.autenticacao.serializers.LoginSerializer",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ["apps.system.assinaturas.tokens.AccessToken"],
    "UPDATE_LAST_LOGIN": True,
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "sub",
    "ISSUER": "api.wcommanda.com.br",
}
