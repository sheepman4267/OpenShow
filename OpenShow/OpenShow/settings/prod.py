from .base import *
import environ

env = environ.Env(
    OPENSHOW_DEBUG=(bool, False),
    OPENSHOW_ALLOWED_HOSTS=(list, []),
    OPENSHOW_REDIS_HOST=(str, None),
    OPENSHOW_REDIS_PORT=(int, 6379),
    OPENSHOW_EVENTSTREAM_REDIS_DB=(int, 0),
    OPENSHOW_TASKS_REDIS_DB=(int, 1),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('OPENSHOW_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('OPENSHOW_DEBUG')

ALLOWED_HOSTS = env('OPENSHOW_ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = ['https://' + host for host in ALLOWED_HOSTS]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / env('OPENSHOW_SQLITE3_PATH'),
    }
}

STATIC_ROOT = env('OPENSHOW_STATIC_ROOT')

MEDIA_ROOT = env('OPENSHOW_MEDIA_ROOT')
MEDIA_URL = '/media/'

EVENTSTREAM_REDIS = {
    "host": env('OPENSHOW_REDIS_HOST'),
    "port": env('OPENSHOW_REDIS_PORT'),
    "db": env('OPENSHOW_EVENTSTREAM_REDIS_DB'),
}

TASKS = {
    "default": {
        "BACKEND": "django_tasks_redis.RedisTaskBackend",
        "QUEUES": [],
        "OPTIONS": {
            "REDIS_HOST": env("OPENSHOW_REDIS_HOST"),
            "REDIS_PORT": env("OPENSHOW_REDIS_PORT"),
            "REDIS_DB": env("OPENSHOW_TASKS_REDIS_DB"),
            "REDIS_BLOCK_TIMEOUT": 100,
        }
    }
}
