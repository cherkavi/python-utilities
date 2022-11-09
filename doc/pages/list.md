# list

## list sort

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/list/list-sort.py) -->
<!-- The below code snippet is automatically added from ../../python/list/list-sort.py -->
```py
my_list = [5,4,2,1]

def get_sort_reverse_function(max_element: int):
    def sort_reverse_function(element) -> int:
        return max_element-element
    return sort_reverse_function

def sort_function(element) -> int:
    return element

my_list.sort(key=get_sort_reverse_function(max(my_list)))
print("reverse sort:"+ str(my_list))

my_list.sort(key=sort_function)
print("sort: "+ str(my_list))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## list substraction via set

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/list/list-substraction-via-set.py) -->
<!-- The below code snippet is automatically added from ../../python/list/list-substraction-via-set.py -->
```py
set1 = set(["a", "b"])
set2 = set(["a"])
print(set1-set2)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## list substraction

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/list/list-substraction.py) -->
<!-- The below code snippet is automatically added from ../../python/list/list-substraction.py -->
```py
files_with_control_date = [each for each in source_list if each not in except_list]


class SubstractAbleList(list):
    def __init__(self, *args):
        super(SubstractAbleList, self).__init__(args)

    def __sub__(self, another_list):
        substracted_list = [each for each in self if each not in antoher_list]
        return self.__class__(*substracted_list)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## list_unpacking

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/list/list_unpacking.py) -->
<!-- The below code snippet is automatically added from ../../python/list/list_unpacking.py -->
```py
from typing import List
from typing import Union

# multi type declaration 
def get_names(prefix: str, names: Union[str, List]) -> Union[str, List]:    
    if isinstance(names, List):
        return [prefix+each_name for each_name in names]
    else:
        return prefix+names

# unpacking 
a,b = get_names("___", ["one", "two"])
c = get_names("___", "figure")

print(a,b,c)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


