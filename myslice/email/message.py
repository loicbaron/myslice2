import smtplib
import premailer

from time import mktime
from datetime import datetime

from tornado import template
from email.utils import formataddr, formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from myslice.email import settings as s
from myslice.email.utils import MessageID

'''
{
    first_name: <string>
    last_name: <string>
    email: <email>
    public_key: <string>
}
'''

class Message(object):
    '''
    Email message object with html, text and attachements.
    '''

    def __init__(self, mail_from=None, mail_to=None, subject=None, plain=None, rich=None, return_path=None, **kw):

        # Default values
        self.mail_from = mail_from
        self.mail_to = mail_to
        self.subject = subject
        self.plain = plain
        self.rich = rich
        
        #
        self.return_path = return_path or self.mail_from[1]
        self.message_id = self._message_id()
        self.date = self._header_date(datetime.now())
        self.encoding = 'utf-8'  
        self.headers = []

        for k in kw:
            if not hasattr(self, k):
                raise AttributeError("Unexpected keyword argument: %s" % k)

            setattr(self, k, kw[k])
    

    def _message_id(self):
        '''
        Initilizes an instance of Message Class.
        Return the message id through __call__.
        '''
        m = MessageID()
        return m()
    
    def _header_date(self, date):
        if isinstance(date, datetime):
            return str(mktime(date.timetuple()))
        if not isinstance(date, basestring):
            return str(formatdate(date, localtime=True))

    def _mime_document(self, plain, rich=None):
        if not rich:
            message = plain

        else:
            message = MIMEMultipart('alternative')
            
            message.attach(plain)
            message.attach(rich)

        return message

    def _builder_headers(self):

        headers = [
                    ('From', self.mail_from),
                    ('To', self.mail_to),
                    ('Subject', self.subject),
                    ('Date', self.date),
                    ('Message-ID', self.message_id),
                    ('Return-Path', self.return_path),
        ]

        return headers

    def _add_headers_to_message(self, headers, message):
        
        for header in headers:
            if header[1] is None and not header[1]:
                continue
            
            name, value = header
            
            if isinstance(value, tuple):
                value = formataddr(value)
            if isinstance(value, list):
                value = ','.join(value)

            message[name] = value

    @property
    def mime(self):
        """Produce the final MIME message."""
        
        if not self.mail_to:
            raise ValueError("You must specify a receiver.")
        
        if not self.subject:
            raise ValueError("You must specify a subject.")

        if not self.plain and not self.rich:
            raise ValueError("You must provide plain text content or rich content.")

        plain = MIMEText(self._callable(self.plain), 'plain', self.encoding)

        rich = None
        if self.rich:
            self.rich = premailer.Premailer(self.rich.decode(self.encoding)).transform()
            rich = MIMEText(self._callable(self.rich), 'html', self.encoding)

        headers = self._builder_headers()
        message = self._mime_document(plain, rich)
        self._add_headers_to_message(headers, message)

        return message

    def as_string(self):
        return self.mime.as_string()

    @staticmethod
    def _callable(var):
        if hasattr(var, '__call__'):
            return var()
        return var

def build_subject_and_template( action, 
                                entity,
                                path=s.email.dir_path,
                                theme=s.email.theme):
    action, entity = str(action), str(entity)

    if action == 'request':
        subject =  'NEW {} REQUEST'.format(entity.upper())
    if action == 'approve':
        subject = 'REQUEST {} APPROVED'.format(entity.upper())
    if action == 'deny':
        subject = 'REQUEST {} DENIED'.format(entity.upper())

    loader = template.Loader(path)
    filename = action + '_email.html'
    temp = loader.load(filename)
    return subject, temp

class Mailer(object):

    def __init__(self):
        #smtp server mailer needs optimatization
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

    def send(self, message):

        self.server.starttls()
        #self.server.set_debuglevel(1)
        self.server.login('zhouquantest16@gmail.com', 'zqtest123')
        self.server.sendmail('zhouquantest16@gmail.com', message.mail_to , message.as_string())
        self.server.quit()

if __name__ == '__main__':
    action, entity = 'request', 'USER'
    subject, temp = build_subject_and_template(action, entity)
    rich = temp.generate(
                                title = subject,
                                entity = entity,
                                theme = s.email.theme,
                                first_name = 'Quan',
                                last_name = 'Zhou',
                                url = "http://oneLab.eu",
                                items = dict(
                                            name = 'Quan Zhou'
                                            ),
                                items_with_buttons = dict(
                                                            name = 'TEST'
                                                        )
                                )

    m = Message(mail_from=('OneLab Support', 'zhouquantest16@gmail.com'),
                mail_to = ['joshzhou16@gmail.com'],
                subject = subject,
                rich = rich
                )

    mailer = Mailer().send(m)

