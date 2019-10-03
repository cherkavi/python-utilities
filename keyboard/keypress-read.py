# keyboard management: 
# * input: getch
# * output: click
# windows: msvcrt

import getch

def waiting_for_key()->[]:
    """
    blocking read from keyboard
    get char from keyboard
    get keytype
    """
    read_symbol_ord = ord(getch.getch())
    if read_symbol_ord == 27:
        return [read_symbol_ord, ord(getch.getch()), ord(getch.getch())]
    else:
        return [read_symbol_ord, ]

while True:
    print(waiting_for_key())
