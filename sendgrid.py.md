```py
# https://github.com/sendgrid/sendgrid-python

import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent, SendGridException

# sending email with python wrappers
API_KEY='SG.PP01jyY-...'
TEMPLATE_ID='d-5015e6...'
sendgrid_client = SendGridAPIClient(os.environ.get(API_KEY))

# web@heritageweb.com
message = Mail(from_email=From('sales@heritagedomainsllc.com', 'heritageweb'), to_emails=To('vitalii.cherkashyn@gmail.com', 'Vitalii'), template=TEMPLATE_ID)

message.template_id = settings.TEMPLATE_ID
# message.dynamic_template_data = {"unsubscribe": "<<< unsubscribe custom text >>>",
#                                  "unsubscribe_preferences": "<<< unsubscribe_preferences custom text >>>"}


try:
    print(json.dumps(message.get(), sort_keys=True, indent=4))
    response = sendgrid_client.send(message=message)
    print(response.status_code)
    print(response.body)
    print(response.headers)        
except SendGridException as e:
    print(e.message)
```

```py
# sending email raw data
sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
data = {
        "personalizations":[
                {
                        "to":[
                                {"email":"vitalii.cherkashyn@gmail.com","name":"Vitalii"}
                        ],
                        "subject":"test sendgrid"
                }
        ],
        "content": [{"type": "text/plain", "value": "Heya!"}],
        "from":{"email":"vitalii.cherkashyn@gmail.com","name":"Vitalii"},
        "reply_to":{"email":"vitalii.cherkashyn@gmail.com","name":"Vitalii"}
}
response = sg.client.mail.send.post(request_body=data)
```