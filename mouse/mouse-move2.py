# pip3 install pynput
# python3
from pynput.mouse import Controller

# move mouse to absolute point 
Controller().position = (50, 50)
# move mouse relatively 
Controller().move(20, 20)
