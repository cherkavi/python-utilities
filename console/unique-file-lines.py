import sys


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
	if len(sys.argv) < 3:
		print(sys.argv)
		print(">>> 'first_file' and [left,right,equals] and 'second_file' files are mandatory")
		sys.exit(1)

	operation = None
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
