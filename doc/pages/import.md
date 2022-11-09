# import

## import module

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/import/import-module/import_module.py) -->
<!-- The below code snippet is automatically added from ../../python/import/import-module/import_module.py -->
```py
# import whole module ( point out to __init__.py)
import some_module as ext_module

if __name__=='__main__':
    ext_module.custom_echo()
    ext_module.custom_print()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## import module

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/import/import-module/some_module/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/import/import-module/some_module/__init__.py -->
```py
# import some function from file1 and make it visible outside
from some_module.file1 import custom_print
# make visible some function from current folder
from some_module.file2 import custom_echo
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## import module

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/import/import-module/some_module/file1.py) -->
<!-- The below code snippet is automatically added from ../../python/import/import-module/some_module/file1.py -->
```py
def custom_print():
    print("print function from module")

def another_not_accessible_outside():
    print("not visible function from outside")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## import module

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/import/import-module/some_module/file2.py) -->
<!-- The below code snippet is automatically added from ../../python/import/import-module/some_module/file2.py -->
```py
def custom_echo():
    print("echo function from module")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## remote import

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/import/remote-import.py) -->
<!-- The below code snippet is automatically added from ../../python/import/remote-import.py -->
```py
# import file/module not in your "classpath"
# import remote file from classpath

##### approach 1.1
import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, '/path/to/application/app/folder')
sys.path.append('/path/to/application/app/folder')
import destination_file

##### approach 1.2
import sys
path_to_site_packages="/opt/homebrew/lib/python2.7/site-packages"  # Replace this with the place you installed facebookads using pip
sys.path.append(path_to_site_packages)
sys.path.append(f"{path_to_site_packages}/facebook_business-3.0.0-py2.7.egg-info")
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

##### approach 2
# from full.path.to.python.folder import func_name
```
<!-- MARKDOWN-AUTO-DOCS:END -->


