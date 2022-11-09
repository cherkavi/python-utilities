# map-reduce-streaming

## mapper

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-streaming/mapper.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-streaming/mapper.py -->
```py
import sys

if __name__=="__main__":
	for line in sys.stdin:
		for each_word in line.strip().split(" "):
			word = each_word.strip()
			if(len(word)>0):
				print(word+"\t1")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## reducer

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-streaming/reducer.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-streaming/reducer.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->


