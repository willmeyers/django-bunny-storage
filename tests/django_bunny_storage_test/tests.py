from hashlib import sha256
from pathlib import Path
from uuid import uuid4

import requests
from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import default_storage
from django.test import SimpleTestCase


class TestBunnyStorage(SimpleTestCase):

    def test_them_all(self):
        test_image = (Path(__file__).parent.parent / 'django_bunny_storage_test_app' / 'media' / 'django.jpeg')

        # that file should not exist in storage
        self.assertFalse(default_storage.exists(f'tmp/{uuid4()}.jpg'))

        with test_image.open('rb') as f:
            test_image_hash = sha256(f.read())
            f.seek(0)
            stored_path = default_storage.save('tmp/django.jpeg', File(f))

        media_url_path = f'{settings.MEDIA_URL}{stored_path}'
        self.assertEquals(default_storage.url(stored_path), f'{settings.MEDIA_URL}{stored_path}')

        media_url_hash = sha256(requests.get(media_url_path).content)

        self.assertTrue(default_storage.exists(stored_path))
        self.assertEquals(default_storage.size(stored_path), test_image.stat().st_size)

        with default_storage.open(stored_path) as stored_file:
            stored_hash = sha256(stored_file.read())

        self.assertEquals(stored_hash.hexdigest(), test_image_hash.hexdigest())
        self.assertEquals(media_url_hash.hexdigest(), test_image_hash.hexdigest())

        default_storage.delete(stored_path)
        self.assertFalse(default_storage.exists(stored_path))
