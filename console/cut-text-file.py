import os
import shutil
import subprocess
import sys

# print part of the file [from line] [to line], 
# bite part of text file

def print_strings_from_file(path_to_file: str, line_begin: int, line_end: int):
    with open(path_to_file) as text_file:
        line_counter = 0
        for each_line in text_file:
            line_counter = line_counter + 1
            if line_begin <= line_counter <= line_end:
                print(each_line, end='')


if __name__ == "__main__":
    if len(sys.argv) < 4: 
        print("expected input parameters: <filename> <number of line_begin> <number of line_end>")
        sys.exit(1)
    if len(sys.argv) == 4:
        print_strings_from_file(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

