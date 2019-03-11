#!/usr/bin/env python

# fuse two files line by line
# when you have one file with lines and another file with respecitve lines - just join them into one

import sys

if __name__=="__main__":
	if len(sys.argv)<3:
		print("expected parameters: {first file} {second file}")
		print("lines in file should be equals")

	f1 = open(sys.argv[1])
	f2 = open(sys.argv[2])

	for f1_line in f1:
		f2_line = f2.readline()
		print("%s\t%s" % (f1_line[:-1], f2_line[:-1]) )

	f1.close()
	f2.close()