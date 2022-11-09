# object-with-properties

## get_attr

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/object-with-properties/get_attr.py) -->
<!-- The below code snippet is automatically added from ../../python/object-with-properties/get_attr.py -->
```py
class CustomAttribute:
	
	def __init__(self):
		print("init")
		self.data = dict()

	def __getattr__(self, prop_name):
		print("get attribute %s " % (prop_name))
		return self.data[prop_name]

	# def __setattr__(self, prop_name, prop_value):
	#	self.data[prop_name] = prop_value

instance = CustomAttribute()

# instance["p1"] = "new value"
# print(instance["p1"])
# print(instance["c2"])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## index object

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/object-with-properties/index-object.py) -->
<!-- The below code snippet is automatically added from ../../python/object-with-properties/index-object.py -->
```py
import sys
import re

def check_function(s, pattern=re.compile(r"[\w/]+:[\w/]+")):
    # regular expression function
    if not pattern.match(s):
        raise TypeError()
    return s

class ArgumentParser:
    """
    simple parser for sys.argv - just allow access by index with "checking type"
    """
    def __init__(self, checking_functions=None):
        self.arguments = sys.argv
        self.checking_functions = checking_functions

    def __getitem__(self, index):
        item = index+1
        if item > len(self.arguments):
            return None
        else:
            if item in self.checking_functions:
                return self.checking_functions[item](self.arguments[item])
            else:
                return self.arguments[item]

if __name__ == '__main__':
    input_arg_parser = ArgumentParser({1: check_function})
    create_image(input_arg_parser[0], input_arg_parser[1], input_arg_parser[2])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## object

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/object-with-properties/object.py) -->
<!-- The below code snippet is automatically added from ../../python/object-with-properties/object.py -->
```py
class ClassExample:
	def __init__(self, value):
		self.__value__ = value
	
	def __str__(self):
		return self.__value__

	def get_data(self):
		return self.__value__

	def set_data(self, new_value):
		self.__value__ = new_value

	def del_data(self):
		del self.__value__
	
        # getter attribute
        @property
	def data2(self):
		return self.__value__
	
	@data2.setter
	def data2(self, new_value):
		self.__value__ = new_value

	data=property(get_data, set_data)
    # data=property(get_data, None)
    # data=property(get_data, set_data, del_data, "full signature for property object")


	@staticmethod
	def description():
		return "static method value"


def print_values(objectInstance):
	print("to string: \n %s " % (objectInstance))
	print("private property: %s" % (objectInstance.__value__) )
	objectInstance.data2 = "new value"
	print("property: %s" % (objectInstance.data))
	print("property  via annotation: %s" % (objectInstance.data2))
	print("static method: %s " % (ClassExample.description()))


print("--- ClassExample ---")
print_values(ClassExample("value for ClassValue"))

class ChildClass(ClassExample):
	def __init__(self, value):
		# ClassExample.__init__(self, value)
		super(ChildClass, self).__init__(value)

print("--- ChildClass ---")
print_values(ChildClass("value for ChildValue"))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## set_attr

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/object-with-properties/set_attr.py) -->
<!-- The below code snippet is automatically added from ../../python/object-with-properties/set_attr.py -->
```py
class CustomAttribute:
	
	def __init__(self):
		# avoid recursion
		super(CustomAttribute, self).__setattr__('data', dict())

	def __getattr__(self, prop_name):
		return self.data[prop_name]

	def __setattr__(self, prop_name, prop_value):
		self.data[prop_name] = prop_value

instance = CustomAttribute()

instance.p1 = "new value for property p1"
print(instance.p1)
try:
	print(instance.c2)
except KeyError as e:
	print("exception: " + str(e))

print(getattr(instance, "p1"))
print(dir(instance))
```
<!-- MARKDOWN-AUTO-DOCS:END -->


