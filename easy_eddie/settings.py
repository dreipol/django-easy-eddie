from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

AWS_DEFAULT_REGION = getattr(settings, 'EASYEDDIE_AWS_DEFAULT_REGION', getattr(settings, 'AWS_DEFAULT_REGION'))
if not AWS_DEFAULT_REGION:
    raise ImproperlyConfigured('Set AWS_DEFAULT_REGION or EASYEDDIE_AWS_DEFAULT_REGION in your settings.')

AWS_ACCESS_KEY_ID = getattr(settings, 'EASYEDDIE_AWS_ACCESS_KEY_ID', getattr(settings, 'AWS_ACCESS_KEY_ID'))
if not AWS_ACCESS_KEY_ID:
    raise ImproperlyConfigured('Set AWS_ACCESS_KEY_ID or EASYEDDIE_AWS_ACCESS_KEY_ID in your settings.')

AWS_SECRET_ACCESS_KEY = getattr(settings, 'EASYEDDIE_AWS_SECRET_ACCESS_KEY', getattr(settings, 'AWS_SECRET_ACCESS_KEY'))
if not AWS_SECRET_ACCESS_KEY:
    raise ImproperlyConfigured('Set AWS_SECRET_ACCESS_KEY or EASYEDDIE_AWS_SECRET_ACCESS_KEY in your settings.')

CLOUD_WATCH_LOG_GROUP_NAMES = getattr(settings, 'EASYEDDIE_CLOUD_WATCH_LOG_GROUP_NAMES')
if not CLOUD_WATCH_LOG_GROUP_NAMES:
    raise ImproperlyConfigured('Set EASYEDDIE_CLOUD_WATCH_LOG_GROUP_NAMES in your settings.')
