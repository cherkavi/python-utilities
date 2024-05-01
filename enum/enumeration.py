import enum

print(">>> just a simple static elements")

class Furniture(enum.Enum):
	Table = 1
	Chair = 2
	Briefcase = 3

print(Furniture.Table)
print(Furniture.Chair)

print(Furniture(2).name)


import enum

print(">>> extends from enumeration")

class WriteTools(enum.Enum):
	# Pencil, Pen = range(2)
	Pencil = 1
	Pen = 2

print(WriteTools.Pencil)
print(WriteTools.Pen.value)



print(">>> enumerations with parameters")
class Angles(enum.Enum):
	Triangle = (3, "three")
	Rectangle = (4, "four")
	Pentagrame = (5, "five")

print("enum value: ", Angles.Triangle.value)
print("enum value type: ", type(Angles.Triangle.value))


print(">>> runtime creation from string")
employee = enum.Enum("Employee", "Jack Ralph Maria")
print(employee)

print(">>> parse enum from string, enum valueof")
parsed_value:Furniture = Furniture["Table"]
print(parsed_value.name)
print(parsed_value.value)

parsed_value:Furniture = Furniture["NotExists"]
print(parsed_value.name)
print(parsed_value.value)
