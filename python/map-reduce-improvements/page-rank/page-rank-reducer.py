import sys

last_index = None
weights = list()
elements = list()

def print_values():
	found_weight = 0
	for index in range(len(weights)):
		if len(elements[index])==2:
			found_weight +=weights[index]
		else:
			found_element = elements[index]
	print("%s\t%.3f\t%s" % (last_index, found_weight,found_element) )


for text_line in sys.stdin:
	line = text_line.strip().split("\t")
	index = line[0]

	if last_index != index:
		if last_index:
			print_values()
		weights = list()
		elements = list()
	last_index = index
	weights.append(float(line[1]))
	elements.append(line[2])
	
print_values()