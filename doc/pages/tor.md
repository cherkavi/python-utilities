# tor

## change tor ip

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/tor/change-tor-ip.py) -->
<!-- The below code snippet is automatically added from ../../python/tor/change-tor-ip.py -->
```py
# pip3 install stem
from stem import Signal
from stem.control import Controller
import os

# generate password ```tor --hash-password mypassword```
# set properties ```sudo vim /etc/tor/torrc```
""" 
ControlPort 9051 
HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7076A3D701ADFDAFDA684053EC4C 
"""
# sudo service tor restart
# export TOR_PASSWORD=mypassword

with Controller.from_port(port = 9051) as controller: #ControlPort 9050 
    try:
        tor_password=os.environ.get("TOR_PASSWORD")
        controller.authenticate(password=tor_password)       
    except Exception as e:
        print(e)
        exit(1)
    print("changing tor-ip address ")
    controller.signal(Signal.NEWNYM)
    print("signal sent ")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## tor signal

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/tor/tor-signal.py) -->
<!-- The below code snippet is automatically added from ../../python/tor/tor-signal.py -->
```py
#  apt-get install tor
#  tor --hash-password mypassword
#  
#  /etc/tor/torrc
#  ControlPort 9051
#  HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C
#
#  sudo service tor restart  (or)  sudo /etc/init.d/tor restart
#
# pip install -U requests 
# pip install requests[socks]

from stem import Signal
from stem.control import Controller
import requests

def get_current_ip():
    proxies = {'http':'socks5h://127.0.0.1:9050', 'https':'socks5h://127.0.0.1:9050'}
    result = requests.get("http://api.ipify.org?format=json",  proxies=proxies)
    # result = requests.get("http://api.ipify.org?format=json")
    return result.text

with Controller.from_port(port = 9051) as controller:
    print(get_current_ip())
    controller.authenticate(password='technik')
    #print("Success!")
    # print(dir(controller))
    controller.signal(Signal.NEWNYM)
    print(get_current_ip())
```
<!-- MARKDOWN-AUTO-DOCS:END -->


