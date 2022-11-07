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
