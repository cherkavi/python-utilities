import sys

if __name__=="__main__":
	current_word = None
	counter = 0

	for line in sys.stdin:
		key_value=line.strip().split("\t")
		key = key_value[0]
		value = key_value[1]
		if(current_word!=key):
			if(current_word):
				print(current_word+"\t"+str(counter))
			current_word=key
			counter=1
		else:
			counter=counter+1
	if(counter>0):
		print(current_word+"\t"+str(counter))

