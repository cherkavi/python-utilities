# map-reduce-improvements

## map reduce combining v1

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/map-reduce-combining-v1.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/map-reduce-combining-v1.py -->
```py
import sys

def increase_word(word_dict, next_word):
    if len(next_word)==0:
        return
    if next_word in word_dict:
        word_dict[next_word] = word_dict[next_word]+1
    else:
        word_dict[next_word] = 1


def map_line(string_with_words):
    words = {}
    for each_word in string_with_words.split(" "):
        increase_word(words, each_word.strip())
    for key,value in words.items():
        print(key+"\t"+str(value))

def main():
    for each_line in sys.stdin:
        map_line(each_line)


if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## map reduce combining v2

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/map-reduce-combining-v2.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/map-reduce-combining-v2.py -->
```py
import sys

def increase_word(word_dict, next_word):
    if len(next_word)==0:
        return
    if next_word in word_dict:
        word_dict[next_word] = word_dict[next_word]+1
    else:
        word_dict[next_word] = 1


def map_line(string_with_words, words):
    for each_word in string_with_words.split(" "):
        increase_word(words, each_word.strip())

def main():
    words = {}
    for each_line in sys.stdin:
        map_line(each_line, words)
    for key,value in words.items():
        print(key+"\t"+str(value))


if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## page rank

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/page-rank/page-rank-mapper.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/page-rank/page-rank-mapper.py -->
```py
import sys


for text_line in sys.stdin:
	line = text_line.strip().split("\t")
	index = line[0]
	weight = line[1]
	elements = sorted(eval(line[2]))
	print(index+"\t"+weight+"\t"+line[2])
	for each_element in elements:
		print(str(each_element)+"\t"+"%.3f\t{}" % round(float(weight)/len(elements),3))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## page rank

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/page-rank/page-rank-reducer.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/page-rank/page-rank-reducer.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/complex-mapper.1.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/complex-mapper.1.py -->
```py
import sys


def main():
    for each_line in sys.stdin:
        words = each_line.strip().split(",")
        print(words[1]+"\t1")

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/complex-mapper.2.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/complex-mapper.2.py -->
```py
import sys


def print_outer_join(values):
    for i in range(len(values)):
        for j in range(len(values)):
            if i!=j and values[i]!=values[j]:
                print(values[i]+","+values[j]+"\t1")

def main():
    for each_line in sys.stdin:
        words = each_line.strip().split(" ")
        print_outer_join(words)

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/complex-mapper.3.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/complex-mapper.3.py -->
```py
import sys

def add_to_stripe(stripe, letter):
    if letter in stripe:
        stripe[letter] = stripe[letter] + 1
    else:
        stripe[letter] = 1

def flat_stripe(stripe):
    return ",".join([ key+":"+str(value) for key,value in stripe.items()])

def print_stripe(letter, stripe):
    print(letter + "\t"+flat_stripe(stripe))

def print_outer_join(values):
    for i in range(len(values)):
        stripe = dict()
        for j in range(len(values)):
            if i!=j and values[i]!=values[j]:
                add_to_stripe(stripe, values[j])
        print_stripe(values[i], stripe)

def main():
    for each_line in sys.stdin:
        words = each_line.strip().split(" ")
        print_outer_join(words)

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/complex-mapper.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/complex-mapper.py -->
```py
import sys


def main():
    for each_line in sys.stdin:
        words = each_line.strip().split("\t")
        count = words[0]
        for letter in  words[1].strip().split(","):
            print(count+","+letter+"\t1") 

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/complex-reducer.1.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/complex-reducer.1.py -->
```py
import sys

def add_to_dictionary(values, letter, count):
    if letter in values:
        values[letter] = values[letter] + int(count)
    else:
        values[letter] = int(count)

def print_dictionary(values):
    for key, value in values.items():
        print(key+"\t"+str(value))


def main():
    values = dict()
    previous_line = None
    for each_line in sys.stdin:
        if previous_line==each_line:
            continue
        words = each_line.strip().split("\t")
        letter = words[1]
        add_to_dictionary(values, letter, 1)
        previous_line = each_line

    print_dictionary(values)

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/complex-reducer.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/complex-reducer.py -->
```py
import sys


def main():
    previous_value = None
    for each_line in sys.stdin:
        words = each_line.strip().split("\t")
        if previous_value!=words[0]:
            if previous_value:
                print(previous_value)
        previous_value = words[0]
    print(previous_value)

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/mapper-filter.1.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/mapper-filter.1.py -->
```py
import sys

def main():
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") if len(each.strip())>0 ]
        print(values[2])

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/mapper-filter.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/mapper-filter.py -->
```py
import sys

def main():
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") if len(each.strip())>0 ]
        if values[1]=="user10":
            print("\t".join(values))

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/reducer-join-inner.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/reducer-join-inner.py -->
```py
import sys

def main():
    last_key = None
    last_letter = None
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") ]
        key = values[0]
        letter = values[1]
        
        if last_key == key:
            if last_letter!=letter:
                print(key)

        last_key = key
        last_letter = letter

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/reducer-join-outer.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/reducer-join-outer.py -->
```py
import sys

def main():
    last_value = None
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") ]
        value = values[0]
        if last_value!=value:
            if last_value:
                print(last_value)
            last_value = value
        print(last_value)

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/reducer-merge.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/reducer-merge.py -->
```py
import sys


def main():
    user_last = None
    query = []
    url = []

    def print_user():
        size = len(query) if len(url)>len(query) else len(url)
        for each_query in query:
            for each_url in url:
                print(user_last + "\t" + each_query + "\t" + each_url)

    for line in sys.stdin:
        input_line = line.split("\t")
        user = input_line[0].strip()
        attributes = input_line[1].split(":")
        attr_name = attributes[0].strip()
        attr_value = attributes[1].strip()
        # print(" >>> " + user + "  " + str(attributes))
        
        if user_last != user:
            print_user()
            user_last = user
            query = []
            url = []
        if attr_name == 'query':
            query.append(attr_value)
        if attr_name == 'url':
            url.append(attr_value)

    if len(query)>0 or len(url)>0:
        print_user()        
        

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/reducer-substract-left.1.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/reducer-substract-left.1.py -->
```py
import sys

def main():
    original_data = []
    
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") ]
        key = values[0]
        letter = values[1]

        if letter == 'A':
            if key not in original_data:
                original_data.append(key)
        else:
            if key in original_data:
                original_data.remove(key)
    for each in original_data:
        print(each)
if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/reducer-substract-left.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/reducer-substract-left.py -->
```py
import sys

def main():
    last_key = None
    last_letter = None
    printed = False
    last_line = None
    for line in sys.stdin:
        if line == last_line:
            continue
        values = [each.strip() for each in line.split("\t") ]
        key = values[0]
        letter = values[1]
        
        if last_key != key:
            if last_letter!=letter:
                print(key)
                printed = True
        else:
            printed = False
        last_key = key
        last_letter = letter
        last_line = line
    if not printed and last_letter=='A':
        print(key)

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## specific

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/specific/reducer-substract-outer.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/specific/reducer-substract-outer.py -->
```py
import sys

def main():
    original_data = []
    last_line = None
    for line in sys.stdin:
        if last_line == line:
            continue
        values = [each.strip() for each in line.split("\t") ]
        key = values[0]
        letter = values[1]

        if key in original_data:
            original_data.remove(key)
        else:
            original_data.append(key)
        last_line = line
    for each in original_data:
        print(each)
if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## tf idf

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/tf-idf/mapper.1.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/tf-idf/mapper.1.py -->
```py
#!/usr/bin/env python3

import sys
import re

def main():
    for line in sys.stdin:
        delimiter = line.find(":")
        if delimiter<=0:
            continue
        document_number = line[0:delimiter]
        # break string to separate words
        # split by words
        words = re.compile(u'\w+', re.UNICODE)
        elements = words.findall(line[delimiter+1:])

        for each_element in elements:
            print(each_element+"#"+document_number+"\t1")

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## tf idf

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/tf-idf/mapper.2.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/tf-idf/mapper.2.py -->
```py
#!/usr/bin/env python3

import sys

def main():
    for line in sys.stdin:
        elements = line.strip().split("\t")
        print(elements[0]+"\t"+elements[1]+";"+elements[2]+";1")

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## tf idf

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/tf-idf/reducer.1.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/tf-idf/reducer.1.py -->
```py
#!/usr/bin/env python3

import sys
import re

def print_value(line, size):
    split = line.split("#")
    print(split[0]+"\t"+split[1]+"\t"+str(size))

def main():
    previous_line = None
    counter = 0
    for each_line in sys.stdin:
        line = each_line.split("\t")[0]
        if previous_line == line:
            counter+=1
        else:
            if previous_line!=None:
                print_value(previous_line, counter)
            counter=1
        previous_line = line
    print_value(previous_line, counter)


if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## tf idf

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce-improvements/tf-idf/reducer.2.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce-improvements/tf-idf/reducer.2.py -->
```py
#!/usr/bin/env python3

import sys


def main():
    previous_word = None
    counter = 0
    to_print = []
    def print_result():
        for each_line in to_print:
            print(each_line+str(counter))

    for each_line in sys.stdin:
        line = each_line.strip().split("\t")
        control_word = line[0]
        elements = line[1].split(";")
        if control_word!=previous_word:
            if previous_word:
                print_result()
            to_print = []
            counter = 0
        counter +=1 
        to_print.append(control_word+"#"+elements[0]+"\t"+elements[1]+"\t")
        previous_word = control_word
    print_result()

if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->


