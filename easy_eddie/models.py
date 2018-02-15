from django.db import models
from django.utils.translation import ugettext_lazy as _


class SMSEvent(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fetched_cloud_watch_log = models.DateTimeField(blank=True, null=True)
    sns_destination = models.CharField(max_length=255)
    sns_dwell_time = models.PositiveIntegerField(blank=True, null=True)
    sns_dwell_time_until_device_acknowledgement = models.PositiveIntegerField(blank=True, null=True)
    sns_mcc = models.PositiveIntegerField(blank=True, null=True)
    sns_message_id = models.CharField(max_length=255, unique=True)
    sns_mnc = models.PositiveIntegerField(blank=True, null=True)
    sns_phone_carrier = models.CharField(blank=True, max_length=255)
    sns_price = models.FloatField(blank=True, null=True)
    sns_provider_response = models.CharField(blank=True, max_length=255)
    sns_sms_type = models.CharField(blank=True, max_length=255)
    sns_status = models.CharField(blank=True, max_length=255)
    sns_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _('SMS Event')
        verbose_name_plural = _('SMS Events')

    def __str__(self):
        return self.sns_message_id
