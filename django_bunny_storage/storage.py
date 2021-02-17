from django.conf import settings
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured

import requests


class BunnyStorage(Storage):
    """ Implementation of Django's storage module using Bunny.net. 
    """

    username: str   = None
    password: str   = None
    region: str     = None

    def __init__(self):
        if not settings.BUNNY_USERNAME:
            raise ImproperlyConfigured('Setting BUNNY_USERNAME is required.')

        if not settings.BUNNY_PASSWORD:
            raise ImproperlyConfigured('Setting BUNNY_PASSWORD is required.')

        if settings.BUNNY_REGION:
            self.region = settings.BUNNY_REGION

        self.username = settings.BUNNY_USERNAME
        self.password = settings.BUNNY_PASSWORD

        self.connection = self._connect()

    def _save(self):
        pass

    def _open(self):
        pass

    def delete(self, name):
        pass

    def exists(self, name):
        pass

    def url(self, name):
        pass
