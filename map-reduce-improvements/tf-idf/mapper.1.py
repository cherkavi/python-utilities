#!/usr/bin/env python3

import sys
import re

def main():
    for line in sys.stdin:
        delimiter = line.find(":")
        if delimiter<=0:
            continue
        document_number = line[0:delimiter]
        # break string to separate words
        # split by words
        words = re.compile(u'\w+', re.UNICODE)
        elements = words.findall(line[delimiter+1:])

        for each_element in elements:
            print(each_element+"#"+document_number+"\t1")

if __name__ == '__main__':
    main()