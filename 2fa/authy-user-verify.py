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

