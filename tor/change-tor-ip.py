from stem import Signal
from stem.control import Controller

with Controller.from_port(port = 9050) as controller:
    # controller.authenticate()
    controller.signal(Signal.NEWNYM)
