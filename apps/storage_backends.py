"""
Custom Django Storage backend for Vercel Blob.

Vercel Blob is NOT S3-compatible, so django-storages' S3 backend won't
work here. This wraps the `vercel_blob` package (unofficial Python
client for Vercel Blob's REST API) in Django's Storage interface.

Docs: https://github.com/SuryaSekhar14/vercel_blob
"""
import os
from io import BytesIO

import vercel_blob
from django.core.files.storage import Storage
from django.conf import settings


class VercelBlobStorage(Storage):
    """
    Django Storage backend backed by Vercel Blob.

    Requires the BLOB_READ_WRITE_TOKEN environment variable to be set
    (Vercel sets this automatically once a Blob store is connected to
    the project).
    """

    def _open(self, name, mode='rb'):
        result = vercel_blob.get(self.url(name))
        if result is None:
            raise FileNotFoundError(f"No such blob: {name}")
        return BytesIO(result)

    def _save(self, name, content):
        content.seek(0)
        data = content.read()
        access = getattr(settings, 'VERCEL_BLOB_ACCESS', 'public')
        result = vercel_blob.put(
            name,
            data,
            {
                'access': access,
                'addRandomSuffix': 'false',
                'allowOverwrite': 'true',
            },
        )
        # Vercel may rewrite the pathname (e.g. namespacing); store what
        # it actually used so url()/exists() stay consistent.
        return result.get('pathname', name)

    def exists(self, name):
        try:
            vercel_blob.head(self.url(name))
            return True
        except Exception:
            return False

    def delete(self, name):
        try:
            vercel_blob.delete([self.url(name)])
        except Exception:
            pass

    def url(self, name):
        base = getattr(settings, 'VERCEL_BLOB_PUBLIC_BASE_URL', '')
        base = base.rstrip('/')
        name = name.lstrip('/')
        return f'{base}/{name}'

    def size(self, name):
        meta = vercel_blob.head(self.url(name))
        return meta.get('size', 0)

    def get_available_name(self, name, max_length=None):
        # We handle overwrite/uniqueness via allowOverwrite above;
        # just return the name unchanged.
        return name