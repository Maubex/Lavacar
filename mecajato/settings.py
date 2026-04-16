from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Segurança ────────────────────────────────────
# Adicionado um valor padrão para não dar erro em desenvolvimento local
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-jneo8fq9-_#3kddovv2^hs!%s5u_fi79%m+&5-%rujrh78up(o')

# DEBUG=True por padrão em desenvolvimento. 
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Permitir localhost por padrão para desenvolvimento
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')

# ── Apps ─────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # MyApps
    'clientes',
    'servicos',
]

# ── Middleware ────────────────────────────────────
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

ROOT_URLCONF = 'mecajato.urls'

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

WSGI_APPLICATION = 'mecajato.wsgi.application'

# ── Banco de dados ────────────────────────────────
# Se houver DATABASE_URL (Produção/Docker), ele usa. 
# Se não houver, ele usa o seu PostgreSQL local (americabd).
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:92u8v2zj@localhost:5432/americabd',
        conn_max_age=600
    )
}

# ── Validação de senha ────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internacionalização ───────────────────────────
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE     = 'America/Sao_Paulo'
USE_I18N      = True
USE_TZ        = True

# ── Arquivos estáticos ────────────────────────────
STATIC_URL       = '/static/'
STATIC_ROOT      = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'templates' / 'static']
if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# ── Mídia ─────────────────────────────────────────
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL  = '/media/'

# ── Chave primária padrão ─────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── CSRF ─────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://lavacar-production.up.railway.app',
    'https://*.railway.app',
]