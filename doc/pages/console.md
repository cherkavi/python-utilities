# console

## autocomplete example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/autocomplete-example.py) -->
<!-- The below code snippet is automatically added from ../../python/console/autocomplete-example.py -->
```py
in/env python

# pip install argcomplete
# .bashrc: 
# ```eval "$(register-python-argcomplete autocomplete-example.py)"```
import argparse
from argcomplete.completers import EnvironCompleter

def main(**args):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['create', 'delete']).completer = ChoicesCompleter(('create', 'delete'))
    parser.add_argument('--timeout', choices=['5', '10', '15'], ).completer = EnvironCompleter
    argcomplete.autocomplete()

    args = parser.parse_args()
    main(**vars(args))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## cut text file

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/cut-text-file.py) -->
<!-- The below code snippet is automatically added from ../../python/console/cut-text-file.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## download file

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/download-file.py) -->
<!-- The below code snippet is automatically added from ../../python/console/download-file.py -->
```py
#!/usr/bin/env python

# download file via http and save it locally

import requests
from tqdm import tqdm

def main():
	url = "http://localhost:8808/published/resources/affin.zip.md5"
	for i in range(1,10):
		response = requests.get(url, stream=True)
		file_name = "affin.zip.md5"+str(i)
		with open(file_name, "wb") as handle:
	    		for data in tqdm(response.iter_content()):
        			handle.write(data)
		print( file_name + " " + response.headers["Content-MD5"])

if __name__=='__main__':
	main()
	
# f0b70d245eae21e9c46bd4b94cad41cc *affin-1482164837000.zip
# 91372ab88e402460f2a832ef2c44a834 *affin-1484662020000.zip

#1482164837000
#1484662020000
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## download zip

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/download-zip.py) -->
<!-- The below code snippet is automatically added from ../../python/console/download-zip.py -->
```py
#!/usr/bin/env python

# download file via http
# ( save via copyfileobj )

import requests
import shutil
import time

def main():
	host="localhost"
	port=8808
	brand_name="mywirecard2go"
	file_name=brand_name+".zip"
	url = "http://%s:%i/published/resources/%s" % (host, port, file_name)
	for i in range(1,3):
		current_time = time.time()
		response = requests.get(url, stream=True)
		local_file_name = file_name+str(i)
		with open(local_file_name, "wb") as output_file:
			response.raw.decode_content = True
			shutil.copyfileobj(response.raw, output_file)
		print( local_file_name + " " + response.headers["Content-MD5"] )
		print( time.time()-current_time)
if __name__=='__main__':
	main()
	
# f0b70d245eae21e9c46bd4b94cad41cc *affin-1482164837000.zip
# 91372ab88e402460f2a832ef2c44a834 *affin-1484662020000.zip

#1482164837000
#1484662020000
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## find in string with option

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/find-in-string-with-option.py) -->
<!-- The below code snippet is automatically added from ../../python/console/find-in-string-with-option.py -->
```py
import sys

# - check line of text for matching with input parameters
# ( parameters can be even variants in list )

def line_contains(line, option):
	if type(option) is list:
		for each_option in option:
                        # index without exception
                        # find in string without exception
			if line.find(each_option)>0:
				return True
		return False
	return line.find(option)>0

	return False

def check_lines_for_matching(lines, *options):
	for each_line in lines:
		result = list()
		for each_option in options:
			result.append(line_contains(each_line, each_option))
		if all(result):
			return True
	return False


if __name__=="__main__":
	print(check_lines_for_matching(["my line "], ["two", "one"], "three"))

	print(check_lines_for_matching([" my line is three "], ["two", "one"], "three"))
	print(check_lines_for_matching([" one of my line is three "], ["two", "one"], "three"))
	print(check_lines_for_matching([" one of my line is two or three "], ["two", "one"], "three"))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## input argument selector

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/input-argument-selector.py) -->
<!-- The below code snippet is automatically added from ../../python/console/input-argument-selector.py -->
```py
## select arguments from separated comma list
## usage
# python3 input-argument-selector.py prod,staging user1,user2,user3

import os
import sys
from typing import List

def read_input():
    # from getkey import getkey, keys
    return input()

def print_values(values: List[str]):
    counter = 0;
    for each_value in values:
        counter+=1
        print(f"{counter:<3}  {each_value}")

def get_one_parameter(comma_separated_values:str) -> str:
    values:List[str] = comma_separated_values.split(",")
    while True:
        print_values(values)
        choice = read_input()
        if not choice.strip().isnumeric():
            print("not a number, try again")
            continue
        choice_number: int = int(choice.strip())
        if not 1<=choice_number<=len(values):
            print("select value in range ")
            continue
        return values[choice_number-1]


if __name__=="__main__":
    result_arguments:List[str]=list()
    for each_param in sys.argv[1:]:
        result_arguments.append(get_one_parameter(each_param))   
    print(" ".join(result_arguments))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## input_arguments

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/input_arguments.py) -->
<!-- The below code snippet is automatically added from ../../python/console/input_arguments.py -->
```py
# print input arguments

for each_param in sys.argv:
  print(each_param)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## md5 duplication remover

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/md5-duplication-remover.py) -->
<!-- The below code snippet is automatically added from ../../python/console/md5-duplication-remover.py -->
```py
#!/usr/bin/env python

# remove duplication in specified folder
# ( duplication - with equals md5sum )

import logging
import os
import sys
import hashlib


def main(source_folder):
    file_list = dict()
    for each_file in os.listdir(source_folder):
        path_to_file = os.path.join(source_folder, each_file)
        with open(path_to_file, "r") as text_in_file:
            file_hash = hashlib.md5(text_in_file.read().encode("utf-8")).hexdigest()
        if file_hash in file_list:
            file_list[file_hash].append(path_to_file)
        else:
            file_list[file_hash] = [path_to_file]
    for key, value in file_list.items():
        value.pop(0)
        for each_redundant_file in value:
            os.remove(each_redundant_file)


if __name__ == "__main__":
    app_description = """ find duplication of context of files into folder
    ( calculate md5sum for all files )
    remove duplication
    """

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)

    if len(sys.argv) == 0:
        print("folder with files should be specified")
        sys.exit(1)
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print("specified path is not a folder:"+folder)
        sys.exit(2)
    main(folder)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## pipe example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/pipe-example.py) -->
<!-- The below code snippet is automatically added from ../../python/console/pipe-example.py -->
```py
import sys

# read data from stdin
# using application in linux pipe

exclude_start_with = 'INSERT INTO BRAND_SERVER_DATA.DATABASECHANGELOG'
for line in sys.stdin:
	if not line.startswith(exclude_start_with):
		print(line, end="")

		
# read data from stdin at once
# all_lines = sys.stdin.read()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## remove_left

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/remove_left.py) -->
<!-- The below code snippet is automatically added from ../../python/console/remove_left.py -->
```py
#!/usr/bin/env python3

# find occurrence and remove everything from left

import sys

for each_line in sys.stdin:
    index = each_line.find(sys.argv[1])
    if index<0:
        print(each_line, end="")
    else:
        print(each_line[index:], end="")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## remove_right

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/remove_right.py) -->
<!-- The below code snippet is automatically added from ../../python/console/remove_right.py -->
```py
#!/usr/bin/env python3

# find occurrence and remove everything from it

import sys

for each_line in sys.stdin:
    index = each_line.find(sys.argv[1])
    if index<0:
        print(each_line, end="")
    else:
        print(each_line[0:index], end="")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## return_result_emulator

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/return_result_emulator.py) -->
<!-- The below code snippet is automatically added from ../../python/console/return_result_emulator.py -->
```py
#!/usr/bin/env python3
import argparse
import datetime
'''
emulator of long-running application
settings file contains three lines:
1) answer before time out
2) predefined time
3) answer after time out
'''

def main(file_lines):
    # print(file_lines)
    answer_before = file_lines[0]
    answer_after = file_lines[2]
    time_frontier = datetime.datetime.strptime(file_lines[1], "%H:%M")

    # difference between time only, compare time
    time_to_compare = datetime.time(time_frontier.hour, time_frontier.minute, 0)
    time_now = datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute, 0)

    # print(time_to_compare, time_now)
    if time_now>time_to_compare:
        print(answer_after)
    else:
        print(answer_before)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='read settings file and return first or third strings depends on timeout ')
    parser.add_argument('--settings_file',
                        help='three line file: 1) current return 2) time (20:35) when return third line 3) line with answer after timeout',
                        required=True)
    args = parser.parse_args()
    
    lines = list()
    with open(args.settings_file) as settings_file:
        for line in settings_file:
            clear_line = line.strip()
            if len(clear_line)>0:
                lines.append(clear_line)
    main(lines)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## return_result_waiting

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/return_result_waiting.py) -->
<!-- The below code snippet is automatically added from ../../python/console/return_result_waiting.py -->
```py
#!/usr/bin/env python3
import subprocess
import re
import time
import sys


def run_command_find_answer(command, prefix, suffix):
    '''
    run console command, read result of console command,
    parse console output and find string between markers
    return None when marker was not found
    '''
    process_output = subprocess.check_output(command, shell=False).decode("utf-8")
    result = re.search(prefix+"(.*)"+suffix, process_output)
    if len(result.groups())>0:
        return result.group(1)
    else:
        return None

if __name__ == '__main__':
    command = "./return_result_emulator.sh"
    attempts = 100
    sleep_time = 30

    for _ in range(attempts):
        # print(script_response.groups())
        result = run_command_find_answer(command, ">>>","<<<")
        if not result:
            # print("marker was not found")
            sys.exit(1)                
        if result == "RUNNING":
            # print("still running ...")
            time.sleep(sleep_time)
            continue
        if result == "SUCCESS":
            # print("success")
            sys.exit(0)
        if result == "FAIL":
            # print("fail")
            sys.exit(2)
        # unknown return string 
        sys.exit(1) 
    # timeout
    sys.exit(1)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## split text file

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/split-text-file.py) -->
<!-- The below code snippet is automatically added from ../../python/console/split-text-file.py -->
```py
#!/usr/bin/env python3
import os
import shutil
import sys
from typing import List


# list to parts, split list
# split text file to bunch of parts:
# - { text file } { amount of expected parts }
# - { text file } { start line :included } { end line :included }

def count_amount_of_lines(path_to_file):
    with open(path_to_file) as text_file:
        line_counter = 0
        for each_line in text_file:
            if each_line and len(each_line.strip()) > 0:
                line_counter = line_counter + 1
    return line_counter


def check_output_folder(output_folder: str = "parts") -> str:
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    return output_folder


class NamingStrategy:
    def get_part(self, part_number: int) -> str:
        pass


class FixName(NamingStrategy):
    def __init__(self, root_folder: str):
        self.root_folder = root_folder

    def get_part(self, part_number: int) -> str:
        return (self.root_folder + "/part_%s") % (part_number,)


class PredefinedNames(NamingStrategy):

    def __init__(self, root_folder: str, path_to_file: str):
        self.root_folder = root_folder
        self.names: List[str] = list()
        with open(path_to_file, "r") as file_with_names:
            self.names = [each_line.strip() for each_line in file_with_names if len(each_line.strip()) > 0]

    def get_part(self, part_number: int) -> str:
        return self.root_folder + "/" + (
            self.names[part_number] if part_number < len(self.names) else self.names[part_number % len(self.names)])

    @property
    def count(self) -> int:
        return len(self.names)


def split_file_to_parts(path_to_file: str, parts: int, part_naming: NamingStrategy):
    amount_of_lines = count_amount_of_lines(path_to_file)
    part_size = int(amount_of_lines / parts)
    part_size = part_size if part_size > 1 else part_size + 1

    output_file = None
    with open(path_to_file) as text_file:
        line_counter = 0
        for each_line in text_file:
            line_counter = line_counter + 1
            if line_counter % part_size == 1:
                if output_file:
                    output_file.close()
                output_file = open(part_naming.get_part(int(line_counter / part_size)), "w")
            print(each_line, file=output_file, end='')
    output_file.close()


def is_int(value) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("1. expected input parameters: <filename> <output folder> <amount of parts>")
        print("2. expected input parameters: <filename> <output folder> <path to file with names>")
        sys.exit(1)
    filename = sys.argv[1]
    output_folder = sys.argv[2]
    if is_int(sys.argv[3]):
        amount_of_parts = int(sys.argv[3])
        split_file_to_parts(filename, amount_of_parts, FixName(output_folder))
    else:
        path_to_file_with_names = sys.argv[3]
        naming_strategy: PredefinedNames = PredefinedNames(output_folder, path_to_file_with_names)
        split_file_to_parts(filename, naming_strategy.count, naming_strategy)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## string in list

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/string-in-list.py) -->
<!-- The below code snippet is automatically added from ../../python/console/string-in-list.py -->
```py
import sys

if __name__=='__main__':
	""" 
	check input line for existing as a line into file ( as parameter for current script )
	"""
	if len(sys.argv)==0:
		print("file name with list of control values should be specified")
		sys.exit(1)
	with open(sys.argv[1]) as input_file:
		control_list=[each_line.strip() for each_line in input_file.readlines()]

	for each_line in sys.stdin:
		if each_line.strip() in control_list:
			print(each_line.strip())
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## tail_reader

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/tail_reader.py) -->
<!-- The below code snippet is automatically added from ../../python/console/tail_reader.py -->
```py
import sys
import os

# print last lines from file
# ( hard coded to 5 last lines )

def read_tail(file_path, length):
    return_value = list()
    with open(file_path) as data_file:
        for line in data_file:
            return_value.append(line)
            if len(return_value) > length:
                return_value.pop(0)
    return return_value

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print ( "need to specify input file" )
        sys.exit(1)

    file_name = sys.argv[1]
    if not os.path.isfile(file_name):
        raise Exception("file was not found: "+file_name)

    for each_line in read_tail(file_name, 5):
        print each_line[:-1]
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## trim_strings

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/trim_strings.py) -->
<!-- The below code snippet is automatically added from ../../python/console/trim_strings.py -->
```py
#!/usr/bin/env python
# trim string
import sys

for each_line in sys.stdin:
    print(each_line.strip())
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## unique file lines

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/unique-file-lines.py) -->
<!-- The below code snippet is automatically added from ../../python/console/unique-file-lines.py -->
```py
import sys

# boolean comparasion of two text files
# - lines exist in first file and not exist in second
# - lines exist in both files
# - lines exist not exist in first file but exist in second


def read_file_lines(path_to_file):
	with open(path_to_file) as f:
		return [each_line.strip() for each_line in f.readlines()]


def print_list(lines):
	for each_line in lines:
		print(each_line)


def diff_left(list1, list2):
	return [each_line for each_line in list1 if each_line not in list2]


def diff_right(list1, list2):
	return [each_line for each_line in list2 if each_line not in list1]


def diff_eq(list1, list2):
	return [each_line for each_line in list2 if each_line in list1]


if __name__=='__main__':
	if len(sys.argv) <= 3:
		print(sys.argv)
		print(">>> 'first_file' and [left,right,equals] and 'second_file' files are mandatory")
		sys.exit(1)

	left = read_file_lines(sys.argv[1])
	if sys.argv[2] == "equals":
		operation = diff_eq
	elif sys.argv[2] == "left":
		operation = diff_left	
	elif sys.argv[2] == "right":
		operation = diff_right	
	else:
		None
	if not operation:
		print("second operation should be one of [left, right, equals]")
		sys.exit(2)
	right = read_file_lines(sys.argv[3])

	print_list(operation(left, right))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## unique

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/unique.py) -->
<!-- The below code snippet is automatically added from ../../python/console/unique.py -->
```py
import sys

# print unique elements from file
# order is not guarantee !!! ( replace 'set' with 'list')

def main(arguments) :
    if len(arguments) == 0:
        print("name of file should be specified")
        sys.exit(1)
    unique_lines = set()
    with open(arguments[0]) as f:
        for line in f:
            unique_lines.add(line)
    for eachLine in unique_lines:
        print(eachLine[:-1])

if __name__ == "__main__":
    main(sys.argv[1:])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## zip two files

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/console/zip-two-files.py) -->
<!-- The below code snippet is automatically added from ../../python/console/zip-two-files.py -->
```py
#!/usr/bin/env python

# fuse two files line by line
# when you have one file with lines and another file with respecitve lines - just join them into one

import sys

if __name__=="__main__":
	if len(sys.argv)<3:
		print("expected parameters: {first file} {second file}")
		print("lines in file should be equals")

	f1 = open(sys.argv[1])
	f2 = open(sys.argv[2])

	for f1_line in f1:
		f2_line = f2.readline()
		print("%s\t%s" % (f1_line[:-1], f2_line[:-1]) )

	f1.close()
	f2.close()
```
<!-- MARKDOWN-AUTO-DOCS:END -->


