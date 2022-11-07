#!/usr/bin/python -tt
import sys
import string
from string import join



if len(sys.argv) <= 1:
    print("file name should be specified")
    sys.exit(1)

parameters = list()
with open(sys.argv[1]) as f:
    for each_line in f:
        index = each_line.find("--")
        each_line=each_line[:(index-1)]
        parameters.append(each_line)

print(join(parameters, " "))
print()
for parameter in parameters:
    each=parameter.strip()
    if each.endswith(","):
        each=each[0:len(each)-1]
    index = each.index(".")
    if index >= 0:
        print(each[index+1:])
    else:
        print (each)
