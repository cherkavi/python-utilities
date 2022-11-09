code="bwvdgfa"


import requests
import logging

# example of importing, import error
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# requests log, requests investigation, custom logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
# Accept: */*
# Content-Type: application/x-www-form-urlencoded

client_id="dj0yJmk"
client_secret="a871c"
redirect_uri="https://e-176-43.eu-central-1.compute.amazonaws.com"
data=f"code={code}&grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&response_type=code"
url="https://api.login.yahoo.com/oauth2/get_token"
print(requests.post(url, data=data, headers=headers))
