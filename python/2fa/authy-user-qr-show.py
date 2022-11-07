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