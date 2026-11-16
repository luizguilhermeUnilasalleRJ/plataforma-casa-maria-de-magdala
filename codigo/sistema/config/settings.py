"""
Django settings for config project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# SEGURANÇA
# ==========================================================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'chave-provisoria-apenas-para-desenvolvimento-local'
)

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1'
    ).split(',')
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        'CSRF_TRUSTED_ORIGINS',
        ''
    ).split(',')
    if origin.strip()
]


# ==========================================================
# APLICAÇÕES
# ==========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]


# ==========================================================
# MIDDLEWARE
# ==========================================================

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


# ==========================================================
# URLS E TEMPLATES
# ==========================================================

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ==========================================================
# BANCO DE DADOS POSTGRESQL
# ==========================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get(
            'DB_NAME',
            'casa_maria_magdala'
        ),
        'USER': os.environ.get(
            'DB_USER',
            'postgres'
        ),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get(
            'DB_HOST',
            'localhost'
        ),
        'PORT': os.environ.get(
            'DB_PORT',
            '2103'
        ),
        'OPTIONS': {
            'sslmode': os.environ.get(
                'DB_SSLMODE',
                'prefer'
            ),
        },
    }
}


# ==========================================================
# VALIDAÇÃO DE SENHAS
# ==========================================================

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


# ==========================================================
# INTERNACIONALIZAÇÃO
# ==========================================================

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# ==========================================================
# ARQUIVOS ESTÁTICOS
# ==========================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
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


# ==========================================================
# CONFIGURAÇÕES DE PRODUÇÃO
# ==========================================================

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https'
    )

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 3600


# ==========================================================
# E-MAIL
# ==========================================================

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}


# ==========================================================
# LOGIN
# ==========================================================

LOGIN_URL = '/login/'