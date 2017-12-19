class C1:
	def __init__(self, value):
		self.__value__ = value
	
	def __str__(self):
		return self.__value__

	def get_data(self):
		return self.__value__

	def set_data(self, new_value):
		self.__value__ = new_value
	
	data=property(get_data, set_data)
        # data=property(get_data, None)

newObject = C1("hello")
print("------------ \n %s \n %s " % (newObject, newObject.__value__) )
newObject.data=newObject.__value__ * 2
print(newObject.data)		