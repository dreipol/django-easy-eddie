from django.core.management.base import BaseCommand

from easy_eddie.report_fetchers import fetch_logs_of_unprocessed_sms_events


class Command(BaseCommand):
    help = 'Fetches log data from CloudWatch for all unprocessed SMS events.'

    def handle(self, *args, **options):
        fetch_logs_of_unprocessed_sms_events()
