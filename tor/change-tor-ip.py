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
