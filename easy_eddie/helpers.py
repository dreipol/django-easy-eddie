from datetime import timedelta

from typing import List, Tuple

from easy_eddie.models import SMSEvent


def get_cloud_watch_filter_pattern(sms_events: List[SMSEvent]) -> str:
    """
    Returns the filter pattern needed by AWS CloudWatch for a list of SMSEvent.

    Example:
    '{ $.notification.messageId = <message_id_1> || $.notification.messageId = <message_id_2> }'

    :param sms_events: list
    :return: aws_filter_pattern: str
    """
    aws_message_filter = ['$.notification.messageId = "%s"' % sms_event.sns_message_id for sms_event in sms_events]
    aws_filter_pattern = '{ %s }' % ' || '.join(aws_message_filter)
    return aws_filter_pattern


def get_cloud_watch_time_tuple_for_sms_events(sms_events: List[SMSEvent]) -> Tuple[int, int]:
    """
    Returns the start and end date for a list of SMSEvents.

    :param sms_events: list
    :return: start: datetime, end: datetime
    """
    creation_dates = [sms_event.created for sms_event in sms_events]

    if not creation_dates:
        return 1, 1

    # Sort the creation dates
    creation_dates.sort()

    # We don't know the actual publication date of our messages.
    # To catch all events we add/subtract one day to the filter.
    start = creation_dates[0] - timedelta(days=1)
    end = creation_dates[-1] + timedelta(days=1)

    # Transform to integer timestamp milliseconds
    start = int(start.timestamp() * 1000)
    end = int(end.timestamp() * 1000)

    return start, end
