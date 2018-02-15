from django.core.management.base import BaseCommand

from easy_eddie.models import SMSEvent
from easy_eddie.report_fetchers import fetch_log_events
from easy_eddie.settings import CLOUD_WATCH_LOG_GROUP_NAMES


class Command(BaseCommand):
    help = 'Fetches log data from CloudWatch for all SMS events.'

    def handle(self, *args, **options):
        sms_events = SMSEvent.objects.filter(fetched_cloud_watch_log__isnull=True)
        fetch_log_events(sms_events=sms_events, log_group_names=CLOUD_WATCH_LOG_GROUP_NAMES)
