# https://github.com/kcsaff/getkey/blob/master/tools/keys.txt
# read char from keyboard
from getkey import getkey, keys


while True:
    key = getkey()

    if key == keys.UP:
        print("key up")
    elif key == keys.DOWN:
        print("key down")
    elif key == keys.ESCAPE:
        print("key escape")
    elif key == keys.ENTER:
        print("key enter")
    elif key == keys.DELETE:
        print("key delete")
    else:
        print(key, len(key))