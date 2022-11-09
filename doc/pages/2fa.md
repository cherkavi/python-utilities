# 2fa

## authy user qr show

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/2fa/authy-user-qr-show.py) -->
<!-- The below code snippet is automatically added from ../../python/2fa/authy-user-qr-show.py -->
```py
import sys
import os
from authy.api import AuthyApiClient

authy_api = AuthyApiClient(os.environ.get("AUTHY_API_KEY"))

# Available in version 2.2.4+
response = authy_api.users.generate_qr(os.environ.get("AUTHY_USER_ID"), size=200, label="QR for cherkavi-test")
if response.ok():
    print(response.content['qr_code'])
else:
    print(response.content["message"])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## authy user register

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/2fa/authy-user-register.py) -->
<!-- The below code snippet is automatically added from ../../python/2fa/authy-user-register.py -->
```py
import os
import sys
from authy.api import AuthyApiClient

# Your API key from twilio.com/console/authy/applications
# DANGER! This is insecure. See http://twil.io/secure
authy_api = AuthyApiClient(os.environ.get("AUTHY_API_KEY"))

email = sys.argv[1]        # 'some_email@gmail.com'
phone = sys.argv[2]        # '135 35 35 35 35'
# https://github.com/twilio/authy-form-helpers/blob/master/src/form.authy.js
country_code = sys.argv[3] # 49

user = authy_api.users.create(email=email,phone=phone,country_code=country_code) 
if user.ok():
    print(user.id) # user.id is the `authy_id` needed for future requests    
else:
    print(user.errors())
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## authy user status

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/2fa/authy-user-status.py) -->
<!-- The below code snippet is automatically added from ../../python/2fa/authy-user-status.py -->
```py
from authy.api import AuthyApiClient
import pprint
import os

# check client status
authy_api = AuthyApiClient(os.environ.get("AUTHY_API_KEY"))
status = authy_api.users.status(os.environ.get("AUTHY_USER_ID"))
if status.ok():
    print("OK")
else:
    print("---ERROR---")
pprint.PrettyPrinter(indent=4).pprint(status)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## authy user verify

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/2fa/authy-user-verify.py) -->
<!-- The below code snippet is automatically added from ../../python/2fa/authy-user-verify.py -->
```py
import sys
import os
from authy.api import AuthyApiClient

authy_api = AuthyApiClient(os.environ.get("AUTHY_API_KEY"))
# sms = authy_api.users.request_sms(current_user.authy_id, {'force': True})
# verification = authy_api.phones.verification_check("13535353535","49", sys.argv[1])
verification = authy_api.tokens.verify(token = sys.argv[1], device_id=os.environ.get("AUTHY_USER_ID"))
if verification.ok():
    print("OK")
else:
    print("error")
```
<!-- MARKDOWN-AUTO-DOCS:END -->


