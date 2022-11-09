# generator

## generator_wrapper

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/generator/generator_wrapper.py) -->
<!-- The below code snippet is automatically added from ../../python/generator/generator_wrapper.py -->
```py
class DataApiProxy(object):
    def __init__(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        # raise StopIteration()
        return 1
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## read lines from filelist

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/generator/read-lines-from-filelist.py) -->
<!-- The below code snippet is automatically added from ../../python/generator/read-lines-from-filelist.py -->
```py
import sys

def read_lines(list_of_files):
    def _read_lines():
        for each_file in list_of_files:
            with open(each_file) as current_file:
                yield from current_file
    yield from enumerate(_read_lines())

if __name__ == "__main__":
    for each_line in read_lines(sys.argv[1:]):
        print(each_line)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


