#!/usr/bin/env python3
class ObjectList:

	def __init__(self):
		self.index=0

	def __iter__(self):
		return self

	def __next__(self):
		self.index+=1
		if self.index>5:
			raise StopIteration()
		else:
			return self.index

print(">>> for <<<")
for i in ObjectList():
	print(i)

print(">>> for with iter object <<<")
for i in iter(ObjectList()):
	print(i)

print(">>> for with iter object with limit <<<")
for i in iter(ObjectList().__next__,3):
	print(i)


# ---------------------------------------------

class Iterable:

	def __init__(self):
		self.value = 0

	def next(self):
		self.value+=1
		return self.value


print(">>> for with iter object with limit <<<")
for i in iter(Iterable().next,3):
	print(i)

# ----------------------------------------------

print("execute 'next' function over 'ObjectList'")
values = ObjectList()
print (next(values))
print (next(values))
print (next(values))
