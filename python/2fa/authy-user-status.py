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

