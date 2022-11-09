import sys


for text_line in sys.stdin:
	line = text_line.strip().split("\t")
	index = line[0]
	weight = line[1]
	elements = sorted(eval(line[2]))
	print(index+"\t"+weight+"\t"+line[2])
	for each_element in elements:
		print(str(each_element)+"\t"+"%.3f\t{}" % round(float(weight)/len(elements),3))
