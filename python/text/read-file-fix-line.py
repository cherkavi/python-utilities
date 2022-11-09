textFile=open("array-slicing.py")
for eachLine in textFile :
    value =eachLine
    if value.endswith('\n'):
        value=value[0:-1]
    print value
textFile.close()
