from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from easy_eddie.models import SMSEvent
from easy_eddie.report_fetchers import fetch_log_events
from easy_eddie.reports import get_sms_event_report
from easy_eddie.settings import CLOUD_WATCH_LOG_GROUP_NAMES


class SMSEventAdmin(admin.ModelAdmin):
    actions = ['download_csv_report_action', 'fetch_log_events_action']
    date_hierarchy = 'updated'
    fieldsets = (
        (_('Meta'), {
            'fields': (('created', 'updated'), ('sns_timestamp', 'fetched_cloud_watch_log'), 'sns_message_id',
                       'sns_destination', 'event_name')
        }),
        (_('Detail'), {
            'fields': (('sns_status', 'sns_sms_type'), 'sns_provider_response', 'sns_phone_carrier', 'sns_price',
                       ('sns_dwell_time', 'sns_dwell_time_until_device_acknowledgement'),
                       ('sns_mcc', 'sns_mnc'))
        }),
    )
    list_display = ('sns_message_id', 'created', 'fetched_cloud_watch_log', 'sns_price', 'sns_status')
    list_filter = ('fetched_cloud_watch_log', 'sns_status')
    search_fields = ['sns_message_id']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

    def download_csv_report_action(self, request, queryset):
        sms_event_report = get_sms_event_report(sms_events=queryset)
        response = HttpResponse(content=sms_event_report.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sms_events.csv"'
        return response

    def fetch_log_events_action(self, request, queryset):
        sms_events = queryset.filter(fetched_cloud_watch_log__isnull=True)

        if sms_events:
            fetch_log_events(sms_events=sms_events, log_group_names=CLOUD_WATCH_LOG_GROUP_NAMES)
            messages.success(request, _('Successfully fetched data from CloudWatch.'))
        else:
            messages.error(request, _('No SMS events fetched from CloudWatch.'))

    download_csv_report_action.short_description = _('Download CSV report for selected events')
    fetch_log_events_action.short_description = _('Fetch log for selected events')


admin.site.register(SMSEvent, SMSEventAdmin)
