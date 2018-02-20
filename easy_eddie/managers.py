from django.db import models


class SMSEventManager(models.Manager):
    def unprocessed(self):
        return self.get_queryset().filter(fetched_cloud_watch_log__isnull=True)
