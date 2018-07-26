print(">>> just a simple static elements")

class Furniture:
	Table = 1
	Chair = 2
	Briefcase = 3

print(Furniture.Table)
print(Furniture.Chair)


print(">>> extends from enumeration")

import enum

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

print(Angles.Triangle.value)
