#!/usr/bin/env python3

# find occurrence and remove everything from left

import sys

for each_line in sys.stdin:
    index = each_line.find(sys.argv[1])
    if index<0:
        print(each_line, end="")
    else:
        print(each_line[index:], end="")
