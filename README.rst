=================
django-easy-eddie
=================

This Django package sends your text messages (SMS) through Amazon SNS and provides reporting helpers.

Sending SMS using the famous boto3 package is easy. Creating usage and billing reports can become tricky especially
if you are using multiple projects on the same AWS account or if you need to split cost in any another way.

Using this package's `send_sms()` function stores an SMS event with the message id in your database and allows you to
fetch meta data (incl. price) through CloudWatch after the submission with a management command. An admin action
allows you to export all events as CSV file.

Quickstart
----------

Install django-easy-eddie::

    pip install django-easy-eddie

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'easy_eddie',
        ...
    )

Configure settings:

.. code-block:: python

    AWS_DEFAULT_REGION = 'eu-west-1'
    AWS_SNS_ACCESS_KEY_ID = 'foo'
    AWS_SNS_SECRET_ACCESS_KEY = 'bar'

    EASYEDDIE_AWS_DEFAULT_REGION = AWS_DEFAULT_REGION
    EASYEDDIE_AWS_ACCESS_KEY_ID = AWS_SNS_ACCESS_KEY_ID
    EASYEDDIE_AWS_SECRET_ACCESS_KEY = AWS_SNS_SECRET_ACCESS_KEY
    EASYEDDIE_CLOUD_WATCH_LOG_GROUP_NAMES = [
        'sns/eu-west-1/000000000000/DirectPublishToPhoneNumber',
        'sns/eu-west-1/000000000000/DirectPublishToPhoneNumber/Failure'
    ]

Migrate your database::

    python manage.py migrate easy_eddie

Sending text messages (SMS):

.. code-block:: python

    from easy_eddie.sms import send_sms

    send_sms(sender='your_SNS_sender_id', phone_number='your_phone_number', message='foo')


Management Command
------------------

This management command can be used to fetch log data from CloudWatch for SMS events. It is probably a good idea to
use it in any scheduled way (e.g. crontab, celery beat, etc.)::

    python manage.py fetch_cloud_watch_log_events


AWS CloudWatch
--------------

For more information about setting up CloudWatch logging in AWS, see `Viewing Amazon CloudWatch Metrics and Logs for SMS Deliveries <https://docs.aws.amazon.com/sns/latest/dg/sms_stats_cloudwatch.html>`_


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
