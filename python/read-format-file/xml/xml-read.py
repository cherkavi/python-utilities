import xmltodict

with open('example.xml') as fd:
    doc = xmltodict.parse(fd.read())

print(doc["data"]["items"]["@size"]) 
print(doc["data"]["items"]["item"][2]) 
