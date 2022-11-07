#!/usr/bin/env python3

# find occurrence and remove everything from it

import sys

for each_line in sys.stdin:
    index = each_line.find(sys.argv[1])
    if index<0:
        print(each_line, end="")
    else:
        print(each_line[0:index], end="")
