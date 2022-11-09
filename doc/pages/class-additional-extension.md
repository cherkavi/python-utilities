# class-additional-extension

## class extends

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/class-additional-extension/class-extends.py) -->
<!-- The below code snippet is automatically added from ../../python/class-additional-extension/class-extends.py -->
```py
#!/usr/bin/python3
from math import *

excluded_methods = ["__module__", "__qualname__"]

# create proxy class
# create class to extend it
def copy_class(clazz):
    # create new class 
    class Substitutor(type):
        
        def __new__(self, name, _, attributes, **kwargs):
            print("__new__ for class: %s   with attributes %s" %(name, attributes))
            # set all attributes with exceptions
            for name, value in attributes.items():
                if name in excluded_methods:
                    continue
                setattr(clazz, name, value)
            return clazz

    return Substitutor



# original class
class Value:
    def __init__(self, x):
        self.x = x

    def __str__(self):
    	return "value: "+str(self.x)

v1 = Value(10)

# additional parameter for class
class Value(metaclass=copy_class(Value)):
    
    def difference(self, value_another):
        return self.x-value_another.x

v2 = Value(35)

print( v1.difference(v2) )
```
<!-- MARKDOWN-AUTO-DOCS:END -->


