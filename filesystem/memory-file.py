import StringIO
# temp file memory file
memfile = StringIO.StringIO()

try:
	memfile.write("hello string")
	memfile.seek(0)
	print(memfile.read())
finally:
	memfile.close()
