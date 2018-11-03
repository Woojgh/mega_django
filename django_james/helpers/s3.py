import os

from django.conf import settings
from django.utils import timezone
from django.utils.deconstruct import deconstructible

@deconstructible
class upload_image_with_custom_uuid(object):
    def __init__(self, uuid):
        self.uuid = uuid

    def __call__(self, *args, **kwargs):
        kwargs['uuid'] = self.uuid
        return upload_image_to(*args, **kwargs)


# Upload images to S3 storage
def upload_image_to(instance, filename, uuid='uuid'):
    filename_base, filename_ext = os.path.splitext(filename)
    today = timezone.now()
    if settings.ENVIRONMENT == 'test':
        return '%s/%s%s' % (
            'test_pictures',
            str(getattr(instance, uuid)) + str(today),
            filename_ext.lower(),
        )
    elif '_thumbnail' in filename_base:
        return '%s/%s%s' % (
            instance.UPLOAD_TO + '_thumb',
            str(getattr(instance, uuid)) + '-thumb' + str(today),
            filename_ext.lower(),
        )
    else:
        return '%s/%s%s' % (
            instance.UPLOAD_TO,
            str(getattr(instance, uuid)) + str(today),
            filename_ext.lower(),
        )
