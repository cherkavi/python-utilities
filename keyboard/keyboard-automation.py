import keyboard
import time

if __name__ == '__main__':

    ### record all input keys
    # recorded: [] = keyboard.record(until='esc')
    # print(recorded)


    keyboard.add_hotkey('alt+p', lambda : print('pressed alt + p'))
    ### waiting for ctrl-c, control c
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        pass

    keyboard.clear_hotkey('alt+p')