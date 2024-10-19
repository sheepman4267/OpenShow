from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5r97wkt$n1_mh3=0=3yv6v=%2g2yes#$&)x8@7--%-(dxl_b08'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.0.11', 'localhost', '192.168.0.35', '192.168.1.124', '192.168.181.198']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'

MEDIA_ROOT = f'{BASE_DIR}/media-root/'
MEDIA_URL = '/media/'
