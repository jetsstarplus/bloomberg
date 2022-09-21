from __future__ import absolute_import, unicode_literals
from django_rq import job

from django.core.mail import EmailMessage
from django.conf import settings



@job('high')
def _sendUserPaymentMail(subject, email_message, user):
    """ A Method for sending the user an email incase of an payment"""
    message = EmailMessage(subject, email_message,  'Payment Successful <{}>'.format(settings.DEFAULT_FROM_EMAIL), [user,])
    message.content_subtype = 'plain'
    print('sending')
    message.send()

def sendUserPaymentMail(subject, email_message, user):
    """Calling the task for sending the user payment mail"""
    _sendUserPaymentMail.delay(subject, email_message, user)


@job('high')
def _sendAdminPaymentMail(subject, email_message, user):
    """ A Method for sending the user an email incase of an payment"""
    message = EmailMessage(subject, email_message,  'Payment Received <{}>'.format(settings.DEFAULT_FROM_EMAIL), user)
    message.content_subtype = 'plain'
    message.send()

def sendAdminPaymentMail(subject, email_message, user):
    """Calling the task for sending the user payment mail"""
    _sendAdminPaymentMail.delay(subject, email_message, user)

# sendAdminPaymentMail('hello', 'hi', 'test@example.com')
