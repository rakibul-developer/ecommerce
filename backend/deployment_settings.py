import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR, INSTALLED_APPS

# ----------------------------
# Security & Host Config
# ----------------------------
ALLOWED_HOSTS = [os.environ.get("RENDER_EXTERNAL_HOSTNAME")]
CSRF_TRUSTED_ORIGINS = [f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"] # noqa

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")

# ----------------------------
# Middleware (with WhiteNoise)
# ----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------
# Database (Postgres on Render)
# ----------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ----------------------------
# Static & Media (Cloudinary for media)
# ----------------------------
STORAGES = {
    'default': {  # MEDIA
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {  # STATIC
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# WhiteNoise static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / 'static']  # dev-time static files

# production-ready static files
STATIC_ROOT = BASE_DIR / "staticfiles"


# Cloudinary Config
INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': os.environ.get("CLOUDINARY_API_KEY"),
    'API_SECRET': os.environ.get("CLOUDINARY_API_SECRET"),
}

# Default file storage will now use Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
