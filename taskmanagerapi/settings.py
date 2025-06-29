"""
Django settings for taskmanagerapi project.

Generated by 'django-admin startproject' using Django 5.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import mongoengine
import os

from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")

# Conexión a MongoDB Atlas
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_DB_HOST = os.getenv("DATABASE_HOST")
MONGO_DB_PORT = int(os.getenv("DATABASE_PORT"))
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")

PREFIX_DB = (
    "mongodb"
    if "localhost" in MONGO_DB_HOST or "taskmanagerdb" in MONGO_DB_HOST
    else "mongodb+srv"
)
OPTIONS_DB = (
    "?retryWrites=true"
    if "localhost" in MONGO_DB_HOST or "taskmanagerdb" in MONGO_DB_HOST
    else "?retryWrites=true&w=majority&appName=task-manager-cluster"
)
ADD_DB_PORT = f":{MONGO_DB_PORT}" if "localhost" in MONGO_DB_HOST else ""
CONNECTION_STRING = (
    f"{PREFIX_DB}://{MONGO_DB_HOST}{ADD_DB_PORT}/{MONGO_DB_NAME}{OPTIONS_DB}"
)

print(CONNECTION_STRING)

if MONGO_DB_HOST and MONGO_DB_NAME and ENV == "PROD":
    mongoengine.connect(
        db=MONGO_DB_NAME,
        host=CONNECTION_STRING,
        username=MONGO_DB_USERNAME,
        password=MONGO_DB_PASSWORD,
        alias="default",
        tls=True,
        tlsAllowInvalidCertificates=False,
    )

if MONGO_DB_HOST and MONGO_DB_NAME and ENV != "PROD":
    mongoengine.connect(
        db=MONGO_DB_NAME,
        host=CONNECTION_STRING,
        alias="default",
    )

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if ENV == "PROD" else True

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", default="*").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "accounts",
    "tasks",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "taskmanagerapi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "taskmanagerapi.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.authentication.MongoUserJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "",
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in CORS_ALLOWED_ORIGINS if origin.strip()
]


CORS_ALLOW_CREDENTIALS = True

SPECTACULAR_SETTINGS = {
    "TITLE": "Mi Task Manager API",
    "DESCRIPTION": "Documentación de mi API RESTful con Django REST Framework la cual gestiona la creación de tareas",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SECURITY": [
        {
            "CookieAuth": [],
        }
    ],
    "COMPONENTS": {
        "securitySchemes": {
            "CookieAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "token",
                "description": 'Autenticación por token JWT en cookie. Por favor, inicia sesión para obtener un token en la cookie "token".',
            }
        }
    },
}
