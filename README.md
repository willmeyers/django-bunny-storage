# django-bunny-storage

Provides Bunny.net file storage in Django.

## Installation

`django-bunny-storage` requires Python >= 3.7.

```bash
pip install django-bunny-storage
```

## Configuration

Everything is configured in your `settings.py` file.

To use:

1. Add `django_bunny_storage` to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    'django_bunny_storage'
]
```

2. Add `BUNNY_USERNAME` and `BUNNY_PASSWORD` to your settings.

```python
BUNNY_USERNAME = 'myzone'

BUNNY_PASSWORD = 'myzone-random-password-string'
```

These settings correspond to your storage zone's *Username* and *Password* found under FTP & API Access in your Bunny.net Storage dashboard.

3. Change your default file storage backend.

```python
DEFAULT_FILE_STORAGE = 'django_bunny_storage.storage.BunnyStorage'
```
