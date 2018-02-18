try:
	raise Exception("this is my personal exception")
except Exception as e:
	print(e.args[0])