# django-bunny-storage

Provides Bunny.net file storage in Django.

## Installation

`django-bunny-storage` requires Python >= 3.7.

```bash
pip install django-bunny-storage
```

## Configuration

Everything is configured in your `settings.py` file.

### Enable application

```python
INSTALLED_APPS = [
    ...
    'django_bunny_storage'
]
```

### Set default storage and credentials

```python
# for Django < 4.2
DEFAULT_FILE_STORAGE = 'django_bunny_storage.storage.BunnyStorage'
BUNNY_USERNAME = 'myusername'
BUNNY_PASSWORD = 'my-random-password-string'
BUNNY_PULL_ZONE = 'https://myzone.b-cdn.net/'  # Optional, defaults to MEDIA_URL
BUNNY_REGION = 'de'  # Optional

# for Django >= 4.2
STORAGES = {
    'default': {
        'BACKEND': 'django_bunny_storage.storage.BunnyStorage',
        'OPTIONS': {
            'username': 'myusername',
            'password': 'my-random-string-password',
            'pull_zone': 'https://myzone.b-cdn.net',  # Optional, defaults to MEDIA_URL
            'region': 'de'  # Optional
        }
    },
}
```

Username and password can be found under FTP & API Access in your [Storage dashboard](https://dash.bunny.net/storage).

List of available regions can be
found [here](https://docs.bunny.net/reference/put_-storagezonename-path-filename#api-base-endpoint).
Or you can see it also under FTP & API Access as two-letter prefix of hostname. Missing prefix is default `de` region.

You can either set pull zone in storage config or set it to `MEDIA_URL`, depending on your needs.

### Change your media url.

```python
MEDIA_URL = 'https://myzone.b-cdn.net/'
```

The `MEDIA_URL` is set based on a linked Pull Zone that you set up in
the [CDN dashboard](https://dash.bunny.net/storage).
You can use any domain linked to your Pull, either default or custom.

#### In Templates

Correct `MEDIA_URL` or pull zone allows you to use the convenience `url` attribute provided by Django.

```html
<img src="{{ mymodel.file.url }}"/>
```

## Test

Integration tests can be found in `tests` directory. That's a stub application to run Django tests.
The only test tries to upload, download and delete file from storage, so it requires Bunny CDN credentials.

```bash
export BUNNY_USERNAME=myusername
export BUNNY_PASSWORD=my-random-string-password
export MEDIA_URL=https://myzone.b-cdn.net/

cd tests
python manage.py test
```
