import csv
from io import StringIO

from django.utils.translation import ugettext_lazy as _
from typing import List

from easy_eddie.models import SMSEvent


def get_sms_event_report(sms_events: List[SMSEvent]) -> StringIO:
    csv_file = StringIO()
    csv_writer = csv.writer(csv_file)

    # Write column headlines
    csv_writer.writerow([
        _('Timestamp'),
        _('Message ID'),
        _('Status'),
        _('Phone Carrier'),
        _('Destination'),
        _('Price (USD)'),
        _('Dwell Time'),
        _('Dwell Time Until Device Acknowledgement'),
        _('SMS Type'),
        _('Provider Response'),
        _('MCC'),
        _('MNC'),
    ])

    for sms_event in sms_events:
        csv_writer.writerow([
            sms_event.sns_timestamp.isoformat(),
            sms_event.sns_message_id,
            sms_event.sns_status,
            sms_event.sns_phone_carrier,
            sms_event.sns_destination,
            sms_event.sns_price,
            sms_event.sns_dwell_time,
            sms_event.sns_dwell_time_until_device_acknowledgement,
            sms_event.sns_sms_type,
            sms_event.sns_provider_response,
            sms_event.sns_mcc,
            sms_event.sns_mnc,
        ])

    # Seek back to the beginning of the file
    csv_file.seek(0)
    return csv_file
