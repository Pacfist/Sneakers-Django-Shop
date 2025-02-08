import os
from pathlib import Path
import dj_database_url
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/ 'templates'],
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

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(' ')

# CSRF & CORS for Stripe & Render
CSRF_TRUSTED_ORIGINS = [
    "https://your-app.onrender.com",
    "https://your-custom-domain.com",
    "https://api.stripe.com"
]

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_recaptcha',
    'corsheaders',  # Add CORS for Stripe
    'main',
    'goods',
    'users',
    'carts',
    'orders',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Move this up!
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'app.urls'

# Database
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# Static & Media Files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Authentication
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/'

# Stripe Keys (Now from Env Variables)
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# CORS for Stripe
CORS_ALLOWED_ORIGINS = [
    "https://your-app.onrender.com",
    "https://your-custom-domain.com"
]

# Caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / "cache",
    }
}

# Debug Toolbar (Only for Local)
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ["127.0.0.1"]
