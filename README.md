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

# Optional
BUNNY_REGION = 'de'
```

These settings correspond to your storage zone's *Username* and *Password* found under FTP & API Access in your Bunny.net Storage dashboard.

You must include `BUNNY_REGION` if the default region, **NY**, does not match the region you set yourself. 

3. Change your media url and default file storage backend.

```python
DEFAULT_FILE_STORAGE = 'django_bunny_storage.storage.BunnyStorage'

MEDIA_URL = 'https://myzone.b-cdn.net/' # The Pull Zone hostname.
```

The `MEDIA_URL` is set based on a linked Pull Zone that you setup in the Bunny.net dashboard.

#### In Templates

In order to display your media properly in templates, refer to Django's [docs on the MEDIA_URL attribute](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MEDIA_URL) to ensure you're not getting 404s when trying to load media.

Whenever referencing media, do

```html
<img src="{{ MEDIA_URL }}{{ mymodel.file }}" />
```
