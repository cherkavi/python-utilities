# pex

## magic_name

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pex/magic_name/__main__.py) -->
<!-- The below code snippet is automatically added from ../../python/pex/magic_name/__main__.py -->
```py
if __name__=='__main__':
    print("hello from pex")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## naked_example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pex/naked_example/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/pex/naked_example/__init__.py -->
```py

```
<!-- MARKDOWN-AUTO-DOCS:END -->



## naked_example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pex/naked_example/main.py) -->
<!-- The below code snippet is automatically added from ../../python/pex/naked_example/main.py -->
```py
import sys, os
import json

if __name__=='__main__':
    print("hello from pex")
    if len(sys.argv)>1:
        print("attempt to read json file: "+sys.argv[1])
        with open(sys.argv[1], "r") as json_file:
            print(json.load(json_file))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## naked_example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pex/naked_example/setup.py) -->
<!-- The below code snippet is automatically added from ../../python/pex/naked_example/setup.py -->
```py
from setuptools import setup, find_packages

setup(
    name='naked_example',
    version='0.0.1',
    packages=["json", "."],
    package_data={},
    url='',
    license='',
    description='basement for creating PythonEXectuion',
    long_description=''
)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


