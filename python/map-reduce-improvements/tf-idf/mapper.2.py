#!/usr/bin/env python3

import sys

def main():
    for line in sys.stdin:
        elements = line.strip().split("\t")
        print(elements[0]+"\t"+elements[1]+";"+elements[2]+";1")

if __name__ == '__main__':
    main()