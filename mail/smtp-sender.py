import smtplib
from email.mime.text import MIMEText

MAIL_SENDER = 'system@connect.it'
MAIL_RECEIVERS = ['kong@connect.it', 'cage@connect.it']
MAIL_HOST = 'mail.connect.it'
MAIL_PORT = 587
MAIL_USER = '19282@connect.it'
MAIL_PW = 'mysecretpassword'

MAIL_SUBJECT = f'[ScriptError] {os.path.basename(__file__)}'


def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = MAIL_SUBJECT
    msg['From'] = MAIL_SENDER
    msg['To'] = ', '.join(MAIL_RECEIVERS)
    with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(MAIL_USER, MAIL_PW)
        server.send_message(msg)
