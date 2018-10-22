from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

USE_AWS_PROFILE = getattr(settings, 'EASYEDDIE_USE_AWS_PROFILE', False)

AWS_DEFAULT_REGION = getattr(settings, 'EASYEDDIE_AWS_DEFAULT_REGION', getattr(settings, 'AWS_DEFAULT_REGION', None))
if not AWS_DEFAULT_REGION and not USE_AWS_PROFILE:
    raise ImproperlyConfigured('Set AWS_DEFAULT_REGION or EASYEDDIE_AWS_DEFAULT_REGION in your settings.')

AWS_ACCESS_KEY_ID = getattr(settings, 'EASYEDDIE_AWS_ACCESS_KEY_ID', getattr(settings, 'AWS_ACCESS_KEY_ID', None))
if not AWS_ACCESS_KEY_ID and not USE_AWS_PROFILE:
    raise ImproperlyConfigured('Set AWS_ACCESS_KEY_ID or EASYEDDIE_AWS_ACCESS_KEY_ID in your settings.')

AWS_SECRET_ACCESS_KEY = getattr(settings, 'EASYEDDIE_AWS_SECRET_ACCESS_KEY', getattr(settings, 'AWS_SECRET_ACCESS_KEY', None))
if not AWS_SECRET_ACCESS_KEY and not USE_AWS_PROFILE:
    raise ImproperlyConfigured('Set AWS_SECRET_ACCESS_KEY or EASYEDDIE_AWS_SECRET_ACCESS_KEY in your settings.')

CLOUD_WATCH_LOG_GROUP_NAMES = getattr(settings, 'EASYEDDIE_CLOUD_WATCH_LOG_GROUP_NAMES')
if not CLOUD_WATCH_LOG_GROUP_NAMES:
    raise ImproperlyConfigured('Set EASYEDDIE_CLOUD_WATCH_LOG_GROUP_NAMES in your settings.')
