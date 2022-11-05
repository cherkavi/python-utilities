[doc, examples](https://pypi.org/project/twilio/)

```bash
pip install twilio
```

```python
from twilio.rest import Client
account_sid = "ACc7d575e466..."
auth_token = "f174033188f27..."
client = Client(account_sid, auth_token)
# client.http_client.logger.setLevel(logging.INFO)

try:
    message = client.messages.create(
        to="+1540383....", 
        from_="+141531....",
        body="Hello from Python!")
except TwilioRestException as e:
    print(e)

print(message.sid)
```

```python
message.error_code==None
message.error_message==None
```

