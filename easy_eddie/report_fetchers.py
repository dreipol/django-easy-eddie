import json
from datetime import datetime

import pytz
from django.utils.timezone import now
from typing import List

from easy_eddie.clients import get_boto_client
from easy_eddie.helpers import get_cloud_watch_filter_pattern, get_cloud_watch_time_tuple_for_sms_events
from easy_eddie.models import SMSEvent


def fetch_log_events(sms_events: List[SMSEvent], log_group_names: List[str]):
    if not sms_events:
        return False

    client = get_boto_client(service_name='logs')
    start, end = get_cloud_watch_time_tuple_for_sms_events(sms_events=sms_events)
    sms_events_dict = {sms_event.sns_message_id: sms_event for sms_event in sms_events}

    # The filter pattern used to fetch the events must be less than 1024 chars. So we have to split our events into
    # chunks before creating the request.
    sms_event_chunks = get_sms_events_as_chunks(sms_events=sms_events, chunk_size=10)

    for sms_event_chunk in sms_event_chunks:
        for log_group_name in log_group_names:
            paginator = client.get_paginator('filter_log_events')
            response_iterator = paginator.paginate(
                logGroupName=log_group_name,
                startTime=start,
                endTime=end,
                filterPattern=get_cloud_watch_filter_pattern(sms_events=sms_event_chunk),
                interleaved=True,
            )
            for page in response_iterator:
                for event in page.get('events', []):
                    message = json.loads(event['message'])
                    message_id = message['notification']['messageId']

                    sms_event = sms_events_dict.get(message_id)
                    if sms_event:
                        delivery = message.get('delivery', {})
                        sms_event.fetched_cloud_watch_log = now()
                        sms_event.sns_dwell_time = delivery.get('dwellTimeMs')
                        sms_event.sns_dwell_time_until_device_acknowledgement = delivery.get(
                            'dwellTimeMsUntilDeviceAck')
                        sms_event.sns_mcc = delivery.get('mcc')
                        sms_event.sns_mnc = delivery.get('mnc')
                        sms_event.sns_phone_carrier = delivery.get('phoneCarrier', '')
                        sms_event.sns_price = delivery.get('priceInUSD')
                        sms_event.sns_provider_response = delivery.get('providerResponse')
                        sms_event.sns_sms_type = delivery.get('smsType')
                        sms_event.sns_status = message['status']

                        # Format timestamp
                        timestamp = message['notification']['timestamp']
                        naive_datetime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
                        time_zone_aware_timestamp = pytz.utc.localize(naive_datetime)
                        sms_event.sns_timestamp = time_zone_aware_timestamp

                        sms_event.save()


def get_sms_events_as_chunks(sms_events: List[SMSEvent], chunk_size: int):
    for i in range(0, len(sms_events), chunk_size):
        yield sms_events[i:i + chunk_size]
