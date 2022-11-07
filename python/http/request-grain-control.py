import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import RequestException

s = requests.Session()

# authentication
# s.auth = (USER_NAME, PASSWORD)

retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

s.mount('http://', HTTPAdapter(max_retries=retries))

try:
    s.get('http://httpstat.us/500')
except RequestException as ex:
    print(ex)
