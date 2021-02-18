import os
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'test'

USE_TZ = True

TIME_ZONE = 'UTC'


# Bunny.net settings.

BUNNY_USERNAME = os.environ.get('BUNNY_USERNAME')

BUNNY_PASSWORD = os.environ.get('BUNNY_PASSWORD')

BUNNY_REGION = os.environ.get('BUNNY_REGION')

DEFAULT_FILE_STORAGE = "django_bunny_storage.storage.BunnyStorage"


# Application definition

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django_bunny_storage',
    'django_bunny_storage_test_app',
)


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
