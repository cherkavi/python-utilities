#!/usb/bin/python
for i in range(10):
	try:
		if 10/i==2.0:
			break
	except ZeroDivisionError:
		print(1)
else:
	print(2)
		
