import logging
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
from django.core.files.storage import Storage


class BunnyStorage(Storage):
    """ Implementation of Django's storage module using Bunny.net. 
    """
    _log = logging.getLogger(__name__)

    def __init__(self, username: str = None, password: str = None, pull_zone: str = None, region: str = 'de'):
        _username = getattr(settings, 'BUNNY_USERNAME', username)
        if _username is None:
            raise ImproperlyConfigured('Setting BUNNY_USERNAME or OPTIONS.username is required.')

        _password = getattr(settings, 'BUNNY_PASSWORD', password)
        if _password is None:
            raise ImproperlyConfigured('Setting BUNNY_PASSWORD or OPTIONS.password is required.')

        self.pull_base_url = getattr(settings, 'BUNNY_PULL_ZONE', pull_zone) or settings.MEDIA_URL
        if self.pull_base_url is None:
            raise ImproperlyConfigured('Setting BUNNY_PULL_ZONE or OPTIONS.pull_zone or MEDIA_URL is required.')

        storage_zone_host = 'storage.bunnycdn.com'
        if hasattr(settings, 'BUNNY_REGION') and settings.BUNNY_REGION is not None and settings.BUNNY_REGION != 'de':
            storage_zone_host = f'{settings.BUNNY_REGION}.{storage_zone_host}'

        self.storage_base_url = f'https://{storage_zone_host}/{_username}/'

        self._session = requests.Session()
        self._session.headers['AccessKey'] = _password

        self._log.debug('Initialized with storage zone %s and pull zone %s', self.storage_base_url, self.pull_base_url)

    def __request(self, method: str, name: str, **kwargs):
        response = self._session.request(method, self.storage_base_url + name, **kwargs)
        if response.status_code == 401:
            raise ImproperlyConfigured('Failed to authorize to Bunny CDN storage, please check your credentials')

        return response

    def _save(self, name, content):
        resp = self.__request('PUT', name, data=content)

        if resp.ok:
            return name
        else:
            raise RuntimeError(f'Failed to upload file {name}')

    def _open(self, name, mode='rb'):
        resp = self.__request('GET', name, stream=True)

        if resp.status_code == 404:
            raise ValueError(f'File not found: {name}')

        return File(resp.raw)

    def delete(self, name):
        resp = self.__request('DELETE', name)

        if resp.ok:
            return name
        else:
            raise RuntimeError(f'Failed to delete file {name}')

    def exists(self, name):
        resp = self.__request('DESCRIBE', name)

        if resp.status_code == 404:
            return False

        return True

    def size(self, name):
        resp = self.__request('DESCRIBE', name)

        if resp.status_code == 404:
            raise ValueError(f'File not found: {name}')

        return resp.json()['Length']

    def url(self, name):
        return urljoin(self.pull_base_url, name)
