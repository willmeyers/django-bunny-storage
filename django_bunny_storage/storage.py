from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured

import requests


class BunnyStorage(Storage):
    """ Implementation of Django's storage module using Bunny.net. 
    """

    username = None
    password = None
    region = None

    base_url = None
    headers = None

    def __init__(self):
        if not settings.BUNNY_USERNAME:
            raise ImproperlyConfigured('Setting BUNNY_USERNAME is required.')

        if not settings.BUNNY_PASSWORD:
            raise ImproperlyConfigured('Setting BUNNY_PASSWORD is required.')

        self.base_url = ''

        if settings.BUNNY_REGION:
            self.region = settings.BUNNY_REGION

            if self.region == 'de':
                self.base_url += 'https://storage.bunnycdn.com/'
            else:
                self.base_url += f'https://{self.region}.storage.bunnycdn.com/'
        else:
            self.base_url += 'https://storage.bunnycdn.com/'

        self.username = settings.BUNNY_USERNAME
        self.password = settings.BUNNY_PASSWORD

        self.base_url += f'{self.username}/'
        self.headers = {
            'AccessKey': self.password
        }

    def _save(self, name, content):
        resp = requests.put(self.base_url + name, data=content, headers=self.headers)

        return name

    def _open(self, name, mode='rb'):
        resp = requests.get(self.base_url + name, headers=self.headers)

        if resp.status_code == 404:
            raise ValueError('File not found.')

        return File(resp.content)

    def delete(self, name):
        resp = requests.delete(self.base_url + name, headers=self.headers)

        return name

    def exists(self, name):
        resp = requests.get(self.base_url + name, headers=self.headers)

        if resp.status_code == 404:
            return False

        return True
