# text

## clear prefix

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/text/clear-prefix.py) -->
<!-- The below code snippet is automatically added from ../../python/text/clear-prefix.py -->
```py
import sys

exclude_start_with = 'INSERT INTO BRAND_SERVER_DATA.DATABASECHANGELOG'
for line in sys.stdin:
	if not line.startswith(exclude_start_with):
		print(line, end="")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## read file fix line

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/text/read-file-fix-line.py) -->
<!-- The below code snippet is automatically added from ../../python/text/read-file-fix-line.py -->
```py
textFile=open("array-slicing.py")
for eachLine in textFile :
    value =eachLine
    if value.endswith('\n'):
        value=value[0:-1]
    print value
textFile.close()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## unique

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/text/unique.py) -->
<!-- The below code snippet is automatically added from ../../python/text/unique.py -->
```py
import sys

lines = set()
for line in sys.stdin:
    lines.add(line)

for line in lines:
    print(line, end="")
```
<!-- MARKDOWN-AUTO-DOCS:END -->


