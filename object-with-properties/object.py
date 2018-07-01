class ClassExample:
	def __init__(self, value):
		self.__value__ = value
	
	def __str__(self):
		return self.__value__

	def get_data(self):
		return self.__value__

	def set_data(self, new_value):
		self.__value__ = new_value
	
	@property
	def data2(self):
		return self.__value__
	
	@data2.setter
	def data2(self, new_value):
		self.__value__ = new_value

	data=property(get_data, set_data)
        # data=property(get_data, None)

	@staticmethod
	def description():
		return "static method value"


def print_values(objectInstance):
	print("to string: \n %s " % (objectInstance))
	print("private property: %s" % (objectInstance.__value__) )
	print("property: %s" % (objectInstance.data))
	objectInstance.data2 = "new value"
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

