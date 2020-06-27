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
