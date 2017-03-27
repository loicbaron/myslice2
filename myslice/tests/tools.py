import smtplib
from email.mime.multipart import MIMEMultipart
from  email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

def send_email(subject, body, to):

    server = smtplib.SMTP('tibre.lip6.fr')
    fromaddr = "tester@onelab.eu"

    msg = MIMEMultipart()
    msg['From'] = fromaddr

    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    msg['To'] = to

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("config.py", "rb").read())
    encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="config.py"')
    msg.attach(part)

    server.send_message(msg)

