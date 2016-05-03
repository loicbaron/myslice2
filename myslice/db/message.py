import os
import premailer
import smtplib

from myslice import settings as s
from tornado import template

from datetime import datetime
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
                raise entityError("Unexpected keyword argument: %s" % k)

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

        if not self.plain and not self.rich:
            raise ValueError("You must provide plain text content or rich content.")

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
            
            # only for From
            if isinstance(value, tuple):
                value = formataddr(value)
            if isinstance(value, list):
                value = ','.join(value)

            message[name] = value

    @staticmethod
    def _callable(var):
        if hasattr(var, '__call__'):
            return var()
        return var

class PortalMessage(Message):
    '''
    Email message object related with web templates 
    '''

    def __init__(self, author, to, entity, action=None, theme=None, loader_path=None, **kw):
        subject = self._build_title(entity, action) 
        super().__init__(author, to, subject, **kw)
        
        self.loader = template.Loader(loader_path)
        self.theme = theme
        self.action = action
        self.entity = entity

    def _build_title(self, entity, action):
        if action == 'request':
            return 'NEW {} REQUEST'.format(entity.upper())
        if action == 'approve':
            return 'REQUEST {} APPROVED'.format(entity.upper())
        if action == 'deny':
            return 'REQUEST {} DENIED'.format(entity.upper())

    def _build_template(self):
        pass


    def generate_message(self, **kw):
        try:
            filename = self.action + '_email.html'
            html = self.loader.load(filename).generate(
                        title = self.subject,
                        entity = self.entity,
                        theme = self.theme,
                        **kw)
            self.rich = premailer.Premailer(html.decode('utf-8')).transform()
        except Exception as e:
            print(e)

class Mailer(object):

    def __init__(self):
        #smtp server mailer needs optimatization
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

    def send(self, message):

        self.server.starttls()
        #self.server.set_debuglevel(1)
        self.server.login('zhouquantest16@gmail.com', 'zqtest123')
        self.server.sendmail('zhouquantest16@gmail.com', m.to , message.as_string())
        self.server.quit()

if __name__ == '__main__':
    
    
    # for entity in ['user', 'authority', 'slice', 'project']:
    #     m = Message(author=('OneLab Support', 'zhouquantest16@gmail.com'), 
    #                 to='joshzhou16@gmail.com',
    #                 subject='mere a test'
    #                 )                
    #     m.plain = 'yaaaaaaaaaaaaaaaaaaaaa'
    #     # loader is to load the root directory for the html files
    #     loader = template.Loader("/root/intern/myslice/myslice/web/templates/email")
    #     html = loader.load("approve_email.html").generate(
    #                         title = 'A simple Test',
    #                         first_name = 'Quan',
    #                         last_name = 'Zhou',
    #                         theme = 'onelab',
    #                         url = "http://oneLab.eu",
    #                         entity = entity,
    #                         items = dict(
    #                                     name = 'Quan Zhou',
    #                                     authority_hrn = 'onelab.upmc',
    #                                     public_key = '123456789',
    #                                     user_hrn = 'onelab.upmc.zhouquan',
    #                                     ),
    #                         items_with_buttons = dict(
    #                                     name = 'TEST'
    #                                     )
    #         )
    #     # inliner turn css into html file
    #     html = premailer.Premailer(html.decode('utf-8')).transform()
    #     m.rich = html
    m = PortalMessage(author=('OneLab Support', 'zhouquantest16@gmail.com'),
                to = ['joshzhou16@gmail.com', 'chandlerchou@yahoo.com'],
                entity = 'project',
                action = 'request',
                loader_path = s.email.dirpath,
                theme = s.email.theme,
                )
    m.generate_message(
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
    mailer = Mailer().send(m)




