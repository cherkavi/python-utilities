#  apt-get install tor
#  tor --hash-password mypassword
#  
#  /etc/tor/torrc
#  ControlPort 9051
#  HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C
#
#  sudo service tor restart  (or)  sudo /etc/init.d/tor restart
#
#

from stem import Signal
from stem.control import Controller

with Controller.from_port(port = 9051) as controller:
    controller.authenticate(password='technik')
    print("Success!")
    # print(dir(controller))
    controller.signal(Signal.NEWNYM)
    print("New Tor connection processed")
