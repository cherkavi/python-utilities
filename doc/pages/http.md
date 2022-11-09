# http

## check_mock

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/check_mock.py) -->
<!-- The below code snippet is automatically added from ../../python/http/check_mock.py -->
```py
#!/usr/bin/env python
import requests
import socket


def check_positive_get_response(url):
    try:
        response:requests.Response = requests.get(url, timeout=3)
        return 200 <= response.status_code < 300
    except Exception as e:
        return False
    finally:
        if 'response' in locals():
            response.close()


def is_port_open(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    return result == 0


def print_status(name, url, port=0, is_http=True):
    result = check_positive_get_response(url) if is_http else is_port_open(url, port)
    if result:
        print(" %15s  OK" % name)
    else:
        print(" %15s ---ERROR--- " % name)


print_status("activeMQ", "http://localhost:8161")
print_status("ekyc-dii", "http://localhost:9008/__admin/")
print_status("balas", "http://localhost:19006/__admin/")
print_status("elastic-engine", "http://localhost:19004/__admin/")
print_status("cetrel", "http://localhost:19004/__admin/")
print_status("payment-engine", "http://localhost:19001/__admin/")
print_status("risk", "http://localhost:19005/__admin/")
print_status("mindmatics", "http://localhost:19002/__admin/")
print_status("smtp", "127.0.0.1", 6869, False)
print_status("wip", "http://localhost:19000/__admin/")
print_status("brand-server", "http://localhost:9090/status")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## download zip

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/download-zip.py) -->
<!-- The below code snippet is automatically added from ../../python/http/download-zip.py -->
```py
#!/usr/bin/env python
import requests
import shutil
import time

def main():
	host="localhost"
	port=8808
	brand_name="mywcard2go"
	file_name=brand_name+".zip"
	url = "http://%s:%i/published/resources/%s" % (host, port, file_name)
	for i in range(1,3):
		current_time = time.time()
		response = requests.get(url, stream=True)
		local_file_name = file_name+str(i)
		with open(local_file_name, "wb") as output_file:
			response.raw.decode_content = True
			shutil.copyfileobj(response.raw, output_file)
		print( local_file_name + " " + response.headers["Content-MD5"] )
		print( time.time()-current_time)
if __name__=='__main__':
	main()
	
# f0b70d245eae21e9c46bd4b94cad41cc *affin-1482164837000.zip
# 91372ab88e402460f2a832ef2c44a834 *affin-1484662020000.zip

#1482164837000
#1484662020000
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## download

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/download.py) -->
<!-- The below code snippet is automatically added from ../../python/http/download.py -->
```py
#!/usr/bin/env python
import requests
from tqdm import tqdm

def main():
	url = "http://localhost:8808/published/resources/affin.zip.md5"
	for i in range(1,10):
                response:requests.Response = requests.get(url, stream=True)
		file_name = "affin.zip.md5"+str(i)
		with open(file_name, "wb") as handle:
	    		for data in tqdm(response.iter_content()):
        			handle.write(data)
		print( file_name + " " + response.headers["Content-MD5"])

if __name__=='__main__':
	main()
	
# f0b70d245eae21e9c46bd4b94cad41cc *affin-1482164837000.zip
# 91372ab88e402460f2a832ef2c44a834 *affin-1484662020000.zip

#1482164837000
#1484662020000
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## download2

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/download2.py) -->
<!-- The below code snippet is automatically added from ../../python/http/download2.py -->
```py
def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## http request

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/http-request.py) -->
<!-- The below code snippet is automatically added from ../../python/http/http-request.py -->
```py
import urllib2

try:
	url_response = urllib2.urlopen('http://ecsd0010072c.epam.com:9999/__admin/')
	if url_response.getcode() != 200:
		print(" return code is "+str(url_response.getcode()))
	else:
		print("ok");
	// print(dir(url_response))
except Exception as e:
	print("no connection "+e.message)
# print(url_response)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## openshift api

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/openshift-api.py) -->
<!-- The below code snippet is automatically added from ../../python/http/openshift-api.py -->
```py
import subprocess
import sys
import requests
import json
import yaml

# suppress printing warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def clear_binary_line(b_line):
    next_line = b_line.decode('utf-8')
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    return next_line


def get_all_pods(endpoint, namespace, token):
    url = f"{endpoint}/api/v1/namespaces/{namespace}/pods?limit=10&fieldSelector=status.phase%3DRunning"
    response = requests.get(url,
                            verify=False,
                            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    return [each_item['metadata']['name'] for each_item in response.json()['items']]
    # print(response.json()['metadata']['selfLink'])


def create(endpoint, namespace, token, path_to_file):
    url = f"{endpoint}/api/v1/namespaces/{namespace}/pods"
    with open(path_to_file, 'r') as data_file:
        yaml_data = yaml.load(data_file)
    data = json.dumps(yaml_data)
    response = requests.post(url,
                             verify=False,
                             headers={"Authorization": f"Bearer {token}",
                                      "Accept": "application/json",
                                      "Content-Type": "application/json"
                                      },
                             data=data)
    return response.json()


def delete(endpoint, namespace, token, path_to_file):
    with open(path_to_file, 'r') as data_file:
        yaml_data = yaml.load(data_file)
    resource_type = yaml_data['kind'].lower()
    resource_name = yaml_data['metadata']['name']
    url = f"{endpoint}/api/v1/namespaces/{namespace}/{resource_type}s/{resource_name}"
    response = requests.delete(url,
                               verify=False,
                               headers={"Authorization": f"Bearer {token}",
                                        "Accept": "application/json",
                                        "Content-Type": "application/json"
                                        }
                               )
    return response.json


def main():
    token = clear_binary_line(subprocess.check_output(["oc", "whoami", "-t"]))
    if "Error from server" in token:
        print("you must be logged in into OpenShift", file=sys.stderr)
        return False

    status = clear_binary_line(subprocess.check_output(["oc", "status"])).split("\n")[0].split(" ")
    endpoint = status[5]
    namespace = status[2]

    # print(get_all_pods(endpoint, namespace, token))
    print("delete")
    print(delete(endpoint, namespace, token, "/home/projects/current-task/openshift-docker/working-example-pod.yml"))
    print("create")
    print(create(endpoint, namespace, token, "/home/projects/current-task/openshift-docker/working-example-pod.yml"))


if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## request debug

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/request-debug.py) -->
<!-- The below code snippet is automatically added from ../../python/http/request-debug.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## request get

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/request-get.py) -->
<!-- The below code snippet is automatically added from ../../python/http/request-get.py -->
```py
import requests
response: requests.Response = requests.get(url, cookies={"PHPSESSID": php_session_id }, headers={"x-api-key": self._api_key})`
return response.json().get("user_id", None)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## request grain control

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/request-grain-control.py) -->
<!-- The below code snippet is automatically added from ../../python/http/request-grain-control.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## request post

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/request-post.py) -->
<!-- The below code snippet is automatically added from ../../python/http/request-post.py -->
```py
import logging

import requests

_log = logging.getLogger(__name__)

def _check_captcha_via_rest(secret: str, response: str) -> bool:
    fields_to_send = {
        "secret": secret,
        "response": response}
    # response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=fields_to_send, files={os.path.basename(sample): open(sample, "rb")})

    response_raw = requests.post("https://www.google.com/recaptcha/api/siteverify", data=fields_to_send)
    # !!! it will send object as a url encoded string: secret=my_secret&response=99999

    # if you want to send in JSON, requests json, request json
    response_raw = requests.post("https://www.google.com/recaptcha/api/siteverify", data=json.dumps(fields_to_send))


# example
        entity_object:Dict = {"hello":"work"}
        try:
            response: requests.Response = requests.post(self._build_url(resource_type, resource_type_id, sub_resource_type), json=entity_object)
        except RequestException as ex:
            raise ShopifyException(ex)


# post auth basic
        try:
            response: Response = requests.post(self._build_url(dag_name),
                                               json=self._build_body(product_data_api, dag_name),
                                               auth=(self._user, self._password), headers=AirflowEventGenerator.HEADERS)
        except RequestException as ex:
            raise EventGeneratorException(f"airflow execution exception: {ex.message}")
        if not 200 <= response.status_code < 300:
            raise EventGeneratorException(f"airflow execution exception: {response.text}")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## tornado get params

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/tornado-get-params.py) -->
<!-- The below code snippet is automatically added from ../../python/http/tornado-get-params.py -->
```py
app = tornado.web.Application([(r"/file/([a-zA-Z\-0-9\.:,/_]+)", FileHandler, dict(folder=folder)),])

class FileHandler(tornado.web.RequestHandler):
    def get(self, relative_path):
        print(relative_path)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## tornado upload

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/tornado-upload.py) -->
<!-- The below code snippet is automatically added from ../../python/http/tornado-upload.py -->
```py
# uploading file
import tornado.web
import tornado.ioloop

MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB

MAX_STREAMED_SIZE = 1 * GB


@tornado.web.stream_request_body
class MainHandler(tornado.web.RequestHandler):

    def initialize(self):
        print("start upload")

    def prepare(self):
        self.f = open("test.png", "wb")
        self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)

    def post(self):
        print("upload completed")
        self.f.close()

    def put(self):
        print("upload completed")
        self.f.close()

    def data_received(self, data):
        self.f.write(data)


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(7777)
tornado.ioloop.IOLoop.instance().start()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## web

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/http/web.py) -->
<!-- The below code snippet is automatically added from ../../python/http/web.py -->
```py
# pip install webb

from webb import webb

http_address = "http://mail.ru"

webb.get_ip(http_address)
webb.get_whois_data(http_address)
webb.ping(http_address)
webb.traceroute(http_address)
webb.clean_page( webb.download_page(http_address) )

# webb.web_crawl(http_address)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


