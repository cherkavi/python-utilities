from stem import Signal
from stem.control import Controller

# control file
# /etc/tor/torrc
# generate password
# tor --hash-password mypassword
with Controller.from_port(port = 9050) as controller: #ControlPort 9050 
    controller.authenticate(password="technik")       #HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C 
    controller.signal(Signal.NEWNYM)
