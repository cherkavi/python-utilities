# maven-duplication

## duplication

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/maven-duplication/duplication.py) -->
<!-- The below code snippet is automatically added from ../../python/maven-duplication/duplication.py -->
```py
import sys

def stripline(line):
	# scope
	new_line = cut_till_last_colon(line)
	# version
	version = retrieve_after_last_colon(new_line)
	new_line = cut_till_last_colon(new_line)
	# type
	new_line = cut_till_last_colon(new_line)
	
	name = remove_special_symbols(new_line)
	if name is None:
		return None
	return Element(name, version)
	

def remove_special_symbols(line):
	if line is None:
		return None
	return line.lstrip("+- |\\")

def retrieve_after_last_colon(line):
	if line is None:
		return None
	new_line = line
	index = new_line.rfind(":")
	if index<0:
		return None
	return new_line[index+1:]


def cut_till_last_colon(line):
	if line is None:
		return None
	new_line = line
	index = new_line.rfind(":")
	if index<0:
		return None
	return new_line[:index]

class Element:
	def __init__(self, name, version):
		self.name = name
		self.version = version

	def __str__(self):
		return self.name + ":" + self.version

	@staticmethod
	def retrieve_by_name(container, name):
		for each in container:
			if each.name == name:
				return each
		return None


container = set()
for line in sys.stdin:
	if not line.startswith("[INFO]"):
		continue
	if line.find("\)")>0:
		continue
	if line.find("\(")>0:
		continue
	if line.find("<")>0:
		continue
	if line.find("------")>0:
		continue
	value = line[7:]
	value = stripline(value)
	if value is None:
		continue
	exising_element = Element.retrieve_by_name(container, value.name)
	if exising_element is None:
		container.add(value)
		continue

	if exising_element.version != value.version:
		print(">>> ", value.name, value.version, exising_element.version)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


