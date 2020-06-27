import os
from authy.api import AuthyApiClient

# Your API key from twilio.com/console/authy/applications
# DANGER! This is insecure. See http://twil.io/secure
authy_api = AuthyApiClient(os.environ.get("AUTHY_API_KEY"))

user = authy_api.users.create(
    email='some_email@gmail.com',
    phone='135 35 35 35 35',
    country_code=49) # https://github.com/twilio/authy-form-helpers/blob/master/src/form.authy.js

if user.ok():
    print(user.id)
    print(user)
    # user.id is the `authy_id` needed for future requests
else:
    print(user.errors())
