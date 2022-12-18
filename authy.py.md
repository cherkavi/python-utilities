```python
import os
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
```

## Create new user
```bash
pip install authy
```
```python
import os
from authy.api import AuthyApiClient

# Your API key from twilio.com/console/authy/applications
# DANGER! This is insecure. See http://twil.io/secure
authy_api = AuthyApiClient(os.environ['AUTHY_API_KEY'])

user = authy_api.users.create(
    email='vitalii.cherkashyn@gmail.com',
    phone='157 00 00 00 00',
    country_code=49) # https://github.com/twilio/authy-form-helpers/blob/master/src/form.authy.js

if user.ok():
    print(user.id)
    print(user)
    # user.id is the `authy_id` needed for future requests
else:
    print(user.errors())

```

```python
from authy.api import AuthyApiClient

# check client status
authy_api = AuthyApiClient(os.environ['AUTHY_API_KEY'])
status = authy_api.users.status(os.environ["AUTHY_USER_ID"])
if status.ok():
    print("OK")
else:
    print("---ERROR---")
```

