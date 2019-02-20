from typing import Union

from easy_eddie.clients import get_boto_client
from easy_eddie.models import SMSEvent


def send_sms(sender: str, phone_number: str, message: str, sms_type: str = 'Transactional',
             event_name: str = '') -> Union[SMSEvent, bool]:
    client = get_boto_client(service_name='sns')
    response = client.publish(
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': sender
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': sms_type
            }
        },
        PhoneNumber=phone_number,
        Message=message
    )

    if response and response.get('MessageId'):
        return SMSEvent.objects.create(sns_destination=phone_number, sns_message_id=response['MessageId'],
                                       event_name=event_name)

    return False
