import sys

exclude_start_with = 'INSERT INTO BRAND_SERVER_DATA.DATABASECHANGELOG'
for line in sys.stdin:
	if not line.startswith(exclude_start_with):
		print(line, end="")
