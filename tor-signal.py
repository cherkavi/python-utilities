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
