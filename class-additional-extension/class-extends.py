#!/usr/bin/python3
from math import *

excluded_methods = ["__module__", "__qualname__"]

# create proxy class
# create class to extend it
def copy_class(clazz):
    # create new class 
    class Substitutor(type):
        
        def __new__(self, name, _, attrs, **kwargs):
            # set all attributes with exceptions
            for name, value in attrs.items():
                if name in excluded_methods:
                    continue
                setattr(clazz, name, value)
            return clazz

    return Substitutor



# original class
class Value:
    def __init__(self, x):
        self.x = x

# additional parameter for class
class Value(metaclass=copy_class(Value)):
    
    def difference(self, value_another):
        return self.x-value_another.x


print( Value(10).difference(Value(5)) )