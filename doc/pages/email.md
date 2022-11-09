# email

## quoted printable

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/email/quoted-printable.py) -->
<!-- The below code snippet is automatically added from ../../python/email/quoted-printable.py -->
```py
# quoted-printable data
import quopri
str1 = 'äé'
#encoded = quopri.encodestring('äé'.encode('utf-8'))
encoded = quopri.encodestring(str1.encode('utf-8'))
print(encoded)

str2 = '=C3=A4=C3=A9'
decoded_string = quopri.decodestring(str2)
print(decoded_string.decode('utf-8'))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## send cli

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/email/send-cli/main.py) -->
<!-- The below code snippet is automatically added from ../../python/email/send-cli/main.py -->
```py
# This is a sample Python script.
import configparser
import os
import smtplib
import sys
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from typing import Tuple, Optional

from jinja2 import Environment, FileSystemLoader


def email_make_smtp_attachment(path_to_attachment: str) -> MIMEApplication:
    with open(path_to_attachment, 'br') as f:
        part = MIMEApplication(f.read(), Name=basename(path_to_attachment))
    part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(path_to_attachment))
    return part


def email_make_text(text: str) -> MIMEText:
    # part:MIMEText = MIMEText()
    # message.attach(MIMEText(mail_content, 'plain'))

    # part = MIMEApplication(text)
    # part['Content-Type'] = 'text/plain'
    return MIMEText(text, 'plain')


def read_email_parameters(path_to_settings_file: str) -> Tuple:
    """
    read properties file and return template and CV paths
    :param path_to_settings_file:
    :return:
    """
    parser = configparser.RawConfigParser(default_section="default")
    parser.read(path_to_settings_file)
    return (parser.get("message", "template"), parser.get("message", "cv"))


def send_message(mail_server: str,
                 mail_port: int,
                 mail_login: str,
                 mail_password: str,
                 mail_from: str,
                 recipient: str,
                 subject: str,
                 text: str,
                 path_to_attach_pdf: Optional[str]) -> bool:
    """
    :param mail_server
    :param mail_port
    :param mail_login
    :param mail_password
    :param mail_from: - from email address
    :param recipient: - to email address
    :param subject: - subject of email
    :param text: - text of email
    :param path_to_attach_pdf: - path to PDF CV
    :param path_to_attach_doc: - path to DOC CV
    """
    try:
        # client:yagmail.SMTP = yagmail.SMTP(user=mail_login, password=mail_password)
        with smtplib.SMTP(host=mail_server, port=mail_port, timeout=5) as email_sender:
            try:
                email_sender.ehlo()
                email_sender.starttls()
                # email_sender.ehlo()
                email_sender.login(user=mail_login, password=mail_password)
            except smtplib.SMTPHeloError:
                print("The server didn't reply properly to the helo greeting.")
                return False
            except smtplib.SMTPAuthenticationError:
                print("The server didn't accept the username/ password combination.")
                return False
            except smtplib.SMTPNotSupportedError:
                print("The AUTH command is not supported by the server.")
                return False
            except smtplib.SMTPException:
                print("No suitable authentication method was")
                return False

            message = MIMEMultipart()  # MIMEText(body)
            # message['Subject'] = subject
            message['Subject'] = Header(subject, 'utf-8')
            message['From'] = mail_from
            message['To'] = recipient
            # message['Bcc'] = bcc_addrs
            # message['Date'] = formatdate()

            message.attach(email_make_text(text))
            if path_to_attach_pdf:
                message.attach(email_make_smtp_attachment(path_to_attach_pdf))

            email_sender.sendmail(msg=message.as_string(), from_addr=mail_from, to_addrs=[recipient])
        return True
    except smtplib.SMTPServerDisconnected:
        print(f"can't connect to server: {mail_server}:{mail_port}")
        return False
    except Exception as e:
        print(f"general exception: {e}")
        return False


def get_property_file_path(settings_file_path: str) -> str:
    properties_file = settings_file_path
    if not properties_file:
        print("no settings file found: EMAIL_SENDER_SETTINGS ")
        sys.exit(2)
    properties_file = properties_file.strip()
    if not os.path.isfile(properties_file):
        print(f"no settings file found: {properties_file} ")
        sys.exit(3)

    return properties_file


def make_message_text(template_path: str) -> str:
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))
    return template.render(URL=url_to_suggestion)


def read_message_settings(path_to_settings_file: str) -> Tuple:
    """
    read properties file and return template and CV paths
    :param path_to_settings_file:
    :return:
    """
    parser = configparser.RawConfigParser()
    parser.read(path_to_settings_file)
    return (parser.get("message", "template"), parser.get("message", "cv"))


def read_email_settings(path_to_settings_file: str) -> Tuple:
    """
    read properties file and return template and CV paths
    :param path_to_settings_file:
    :return:
    """
    parser = configparser.RawConfigParser()
    parser.read(path_to_settings_file)

    return (parser.get("email", "mail_server"),
            parser.getint("email", "mail_port"),
            parser.get("email", "mail_login"),
            parser.get("email", "mail_password"),
            parser.get("email", "mail_from")
            )


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("expected three parameters: <path to settings file>  <recipient>  <url or text of suggestion>")
        sys.exit(1)
    settings_file_path= sys.argv[1]
    recipient = sys.argv[2]
    url_to_suggestion = sys.argv[3]

    # prepare message
    path_to_template, path_to_cv = read_message_settings(get_property_file_path(settings_file_path))
    message_text = make_message_text(path_to_template)

    mail_server, mail_port, mail_login, mail_password, mail_from = read_email_settings(get_property_file_path(settings_file_path))
    if send_message(mail_server, mail_port, mail_login, mail_password, mail_from, recipient, "Cherkashyn Vitalii", message_text, path_to_cv):
        exit(0)
    else:
        print("!!! sending error !!!")
        exit(1)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## sendgrid

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/email/sendgrid/send_message.py) -->
<!-- The below code snippet is automatically added from ../../python/email/sendgrid/send_message.py -->
```py
import os
import json

import python_http_client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent, SendGridException


API_KEY='Hn6D'
TEMPLATE_ID='bf513'

message = Mail(subject=Subject("my subject"), from_email=From('sales@sender.com', 'sender'), to_emails=To('vitalii.cherkashyn@gmail.com', 'Vitalii'))
# message.template_id=TEMPLATE_ID
# message.dynamic_template_data = {"unsubscribe": "<<< unsubscribe custom text >>>", "unsubscribe_preferences": "<<< unsubscribe_preferences custom text >>>"}
message.content=PlainTextContent("this is test content")
try:
    sendgrid_client = SendGridAPIClient(API_KEY)
    print(json.dumps(message.get(), sort_keys=True, indent=4))
    response = sendgrid_client.send(message=message)
    if 300>response.status_code>=200:
        print(response.status_code)
        print(response.body)
except SendGridException as e:
    print(e.message)
except python_http_client.exceptions.HTTPError as e:
    print(e.body)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


