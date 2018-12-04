
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
