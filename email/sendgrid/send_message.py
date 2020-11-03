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

