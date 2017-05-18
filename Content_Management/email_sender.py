
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives


# class to send mails according to the status of user
class MailSender:

    def __init__(self):
        '''
        initialization of mailing function
        '''


    def mailBodyCreator(self, reqest, data):
        '''
        to generate the mail body
        :param reqest:
        :param data:
        :return:
        '''