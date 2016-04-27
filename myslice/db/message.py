from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.utils import formataddr

import smtplib

class Message(object):
    '''
    Email message object with html,text,and attachements.
    '''

    def __init__(self, author=None, to=None, subject=None, **kw):

        # attributes for database
        self._id = None
        self._processed = False

        # Default values
        self.author = None
        self.to = None
        self.subject = None
        self.date = datetime.now()
        self.rich = None
        self.plain = None
        self.encoding = 'utf-8'
        
        self.headers = []
        # implement it later
        #self.attachements = []

        if author is not None:
            self.author = author

        if to is not None:
            self.to = to

        if subject is not None:
            self.subject = subject

        for k in kw:
            if not hasattr(self, k):
                raise TypeError("Unexpected keyword argument: %s" % k)

            setattr(self, k, kw[k])

    def _mime_document(self, plain, rich=None):
        if not rich:
            message = plain

        else:
            message = MIMEMultipart('alternative')
            message.attach(plain)

            # if not self.embedded:
            message.attach(rich)

            # else:
            #     embedded = MIMEMultipart('related')
            #     embedded.attach(rich)
            #     for attachment in self.embedded:
            #         embedded.attach(attachment)
            #     message.attach(embedded)

        # if self.attachments:
        #     attachments = MIMEMultipart()
        #     attachments.attach(message)
        #     for attachment in self.attachments:
        #         attachments.attach(attachment)
        #     message = attachments

        return message

    @property
    def mime(self):
        """Produce the final MIME message."""
        
        if not self.to:
            raise ValueError("You must specify a receiver.")
        
        if not self.subject:
            raise ValueError("You must specify a subject.")

        if not self.plain:
            raise ValueError("You must provide plain text content.")

        plain = MIMEText(self._callable(self.plain), 'plain', self.encoding)

        rich = None
        if self.rich:
            rich = MIMEText(self._callable(self.rich), 'html', self.encoding)

        message = self._mime_document(plain, rich)
        headers = self._builder_headers()
        self._add_headers_to_message(message, headers)
        self._mime = message

        return message

    def as_string(self):
        return self.mime.as_string()

    def _builder_headers(self):

        headers = [
                    ('From', self.author),
                    ('To', self.to),
                    ('Subject', self.subject),
        ]

        return headers

    def _add_headers_to_message(self, message, headers):
        
        for header in headers:
            if header[1] is None and not header[1]:
                continue
            
            name, value = header
            
            if isinstance(value, list) or isinstance(value, tuple):
                value = formataddr(value)
            message[name] = value

    @staticmethod
    def _callable(var):
        if hasattr(var, '__call__'):
            return var()
        return var

if __name__ == '__main__':
    from tornado import template
    import premailer

    m = Message(author=('OneLab Support', 'zhouquantest16@gmail.com'), 
                to='joshzhou16@gmail.com',
                subject='mere a test')
    m.plain = 'yaaaaaaaaaaaaaaaaaaaaa'
    
    with open('/root/intern/myslice/myslice/web/templates/email/base.html', 'r') as f:
        content = f.read()
    content = premailer.Premailer(content).transform()
    html = template.Template(content).generate(
                        title = 'A simple Test',
                        first_name = 'Quan',
                        theme = 'Onelab'

        )
    m.rich = html

    #smtp server mailer needs optimatization
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()
    #self.server.set_debuglevel(1)
    server.login('zhouquantest16@gmail.com', 'zqtest123')
    server.sendmail('zhouquantest16@gmail.com',['joshzhou16@gmail.com'], m.as_string())
    server.quit()
