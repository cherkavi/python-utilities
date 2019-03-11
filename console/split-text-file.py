#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

# split text file to bunch of parts:
# - { text file } { amount of expected parts }
# - { text file } { start line :included } { end line :included }

def countAmountOfLines(path_to_file):
	with open(path_to_file) as text_file:
		line_counter = 0
		for each_line in text_file:
			line_counter = line_counter+1
	return line_counter


def splitFileStrings(path_to_file, parts):
	amount_of_lines = countAmountOfLines(path_to_file)
	part_size = int(amount_of_lines/parts)
	output_folder = "parts"

	if os.path.exists(output_folder):
		shutil.rmtree(output_folder)
	os.makedirs(output_folder)

	filename = output_folder+"/part_%s"
	output_file = None
	with open(path_to_file) as text_file:
		line_counter = 0
		for each_line in text_file:
			line_counter = line_counter + 1
			if (line_counter % part_size == 1) and ( (int(line_counter/part_size)+1)*part_size < amount_of_lines ):
				if output_file:
					output_file.close()
				output_file = open(filename % (int(line_counter/part_size), ), "w")
			print(each_line, file=output_file, end='')
	output_file.close()


def readFileStrings(path_to_file, line_begin, line_end):
	with open(path_to_file) as text_file:
		line_counter = 0
		for each_line in text_file:
			line_counter = line_counter + 1
			if line_begin<= line_counter <=line_end:
				print(each_line, end='')


if __name__=="__main__":
	if len(sys.argv)<3:
		print("1. expected input parameters: <filename> <amount of parts>")
		print("2. expected input parameters: <filename> <number of line_begin> <number of line_end>")
		sys.exit(1)
	if len(sys.argv) == 3:
		splitFileStrings(sys.argv[1], int(sys.argv[2]))
	if len(sys.argv) == 4:
		readFileStrings(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) )
