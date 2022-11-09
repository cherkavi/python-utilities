# mouse

## mouse automation

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/mouse/mouse-automation.py) -->
<!-- The below code snippet is automatically added from ../../python/mouse/mouse-automation.py -->
```py
# Xlib.error.DisplayConnectionError: Can't connect to display ":1": b'No protocol specified\n'
# temp solution: xhost +


import keyboard
import time
import pyautogui

if __name__ == '__main__':

    ### record all input keys
    # recorded: [] = keyboard.record(until='esc')
    # print(recorded)


    keyboard.add_hotkey('alt+p', lambda : pyautogui.moveRel(100,100))
    ### waiting for ctrl-c, control c
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        pass

    keyboard.clear_hotkey('alt+p')
```
<!-- MARKDOWN-AUTO-DOCS:END -->


