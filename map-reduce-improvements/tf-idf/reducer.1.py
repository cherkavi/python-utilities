#!/usr/bin/env python3

import sys
import re

def print_value(line, size):
    split = line.split("#")
    print(split[0]+"\t"+split[1]+"\t"+str(size))

def main():
    previous_line = None
    counter = 0
    for each_line in sys.stdin:
        line = each_line.split("\t")[0]
        if previous_line == line:
            counter+=1
        else:
            if previous_line!=None:
                print_value(previous_line, counter)
            counter=1
        previous_line = line
    print_value(previous_line, counter)


if __name__ == '__main__':
    main()