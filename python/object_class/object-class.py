# https://docs.python.org/3/reference/datamodel.html?highlight=__add__#special-method-names

class Info:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def replace_object(self, value:str) -> None:
        value = "new value"

    def __repr__(self):
        return "init value is: {}".format(self.value)

    def new_object_with_class(self, new_value):
        return self.__class__(new_value)

    def new_object_with_new(self, new_value):
        return self.__new__(new_value)


info1 = Info("value1")
print(dir(info1))
print(type(info1))
print(info1)
print(repr(info1))
print("--------------")

info2 = info1.new_object_with_class("value2")
print(dir(info2))
print(type(info2))
print(info2)
print(repr(info2))
print("--------------")

info3 = info1.new_object_with_new(Info)
print(dir(info3))
print(type(info3))
#print(info3)
#print(repr(info3))
print("--------------")

a = "my original string"
info1.replace_object(a)
print(a)