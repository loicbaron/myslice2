import smtplib

from datetime import datetime

from tornado import template
from email.utils import formataddr, formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from myslice.email import settings
from myslice.email.utils import MessageID

class Message(object):
    '''
    A container for email infomation
    '''
    encoding = 'utf-8'

    def __init__(self,  mail_from=None, mail_to=[], headers=[],
                        subject='', 
                        text_content='', html_content=''):

        if not mail_from:
            raise Exception('A Sender of email message must be specified.')
        self.mail_from = mail_from

        if not mail_to:
            raise Exception('A Receiver of email meassge must be specified.')
        self.mail_to = mail_to
        
        if not subject:
            raise Exception('A subject of email message must be specified.')
        self.subject = subject

        if not text_content and not html_content:
            raise Exception('Content of email message must be specified.')

        self.text_content = text_content
        self.html_content = html_content
        self.headers = headers

    def _create_headers(self):
        '''
        Create the headers for the message.
        '''

        date = formatdate()
        message_id = MessageID()()
        return_path = self.mail_from

        headers = [
                    ('From', self.mail_from),
                    ('To', self.mail_to),
                    ('Subject', self.subject),
                    ('Date', date),
                    ('Message-ID', message_id),
                    ('Return-Path', return_path),
        ]

        return headers

    def _create_message(self):
        
        msg =  MIMEMultipart('alternative')

        if self.text_content:
            plain = MIMEText(self.text_content, 'plain', self.encoding)
            msg.attach(plain)

        if self.html_content:
            rich = MIMEText(self.html_content, 'html', self.encoding)
            msg.attach(rich)
            
        return msg

    @property
    def mime(self):
        """Produce the final MIME message."""

        msg = self._create_message()

        if not self.headers:
            self.headers = self._create_headers()

        for header in self.headers:
            name, value = header
            
            # this is for 'mail_to'
            if isinstance(value, list):
                value = ','.join(value)

            msg[name] = value

        return msg

    def as_string(self):
        return self.mime.as_string()


def build_subject_and_template( action, 
                                event,
                                path=settings.email.dir_path,
                                theme=settings.email.theme):
    action, entity = str(action), str(event.object.type)

    if action == 'request':
        subject =  'NEW {} REQUEST'.format(entity.upper())
    if action == 'approve':
        subject = 'REQUEST {} APPROVED'.format(entity.upper())
    if action == 'deny':
        subject = 'REQUEST {} DENIED'.format(entity.upper())
    if action == 'password':
        subject = 'RESET PASSWORD'
    if action == 'confirm':
        subject = 'Confirm your email'

    loader = template.Loader(path)
    filename = action + '_email.html'
    temp = loader.load(filename)
    return subject, temp

class Mailer(object):

    def __init__(self):
        #smtp server mailer needs optimatization
        self.server = smtplib.SMTP(settings.email.host, settings.email.port)

    def send(self, message):
        
        self.server.starttls()
        #self.server.set_debuglevel(1)
        self.server.login(settings.email.user, settings.email.password)
        self.server.sendmail(settings.email.sender, message.mail_to , message.as_string())
        self.server.quit()
        

if __name__ == '__main__':
    pass
