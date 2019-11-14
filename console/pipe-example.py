import sys

# read data from stdin
# using application in linux pipe

exclude_start_with = 'INSERT INTO BRAND_SERVER_DATA.DATABASECHANGELOG'
for line in sys.stdin:
	if not line.startswith(exclude_start_with):
		print(line, end="")

		
# read data from stdin at once
# all_lines = sys.stdin.read()
