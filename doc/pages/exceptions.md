# exceptions

## raise exception

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/exceptions/raise-exception.py) -->
<!-- The below code snippet is automatically added from ../../python/exceptions/raise-exception.py -->
```py
try:
	raise Exception("this is my personal exception")
except Exception as e:
	print(e.args[0])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## read_file

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/exceptions/read_file.py) -->
<!-- The below code snippet is automatically added from ../../python/exceptions/read_file.py -->
```py
try:
    f = open('readme.md')
except (ValueError, IOError) as e:
    # just an example of multiply exception
    if isinstance(e, Iterable) and len(e) > 0:
        error_message = e[0].message
    else:
        error_message = e.message
    print( 'can't open the file: %s' % (error_message, ) )
else:
    with f:
        print f.readlines()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## simple extension

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/exceptions/simple-extension.py) -->
<!-- The below code snippet is automatically added from ../../python/exceptions/simple-extension.py -->
```py
class StorageException(Exception):
    def __init__(self, reason: str = ""):
        self.message = reason


class ScreenshotException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"{message}")
```
<!-- MARKDOWN-AUTO-DOCS:END -->


