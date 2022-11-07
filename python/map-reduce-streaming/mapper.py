import sys

if __name__=="__main__":
	for line in sys.stdin:
		for each_word in line.strip().split(" "):
			word = each_word.strip()
			if(len(word)>0):
				print(word+"\t1")