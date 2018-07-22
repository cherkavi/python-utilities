#!/usr/bin/env python3

import sys


def main():
    previous_word = None
    counter = 0
    to_print = []
    def print_result():
        for each_line in to_print:
            print(each_line+str(counter))

    for each_line in sys.stdin:
        line = each_line.strip().split("\t")
        control_word = line[0]
        elements = line[1].split(";")
        if control_word!=previous_word:
            if previous_word:
                print_result()
            to_print = []
            counter = 0
        counter +=1 
        to_print.append(control_word+"#"+elements[0]+"\t"+elements[1]+"\t")
        previous_word = control_word
    print_result()

if __name__ == '__main__':
    main()