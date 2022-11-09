# read-format-file

## ini

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/read-format-file/ini/ini.py) -->
<!-- The below code snippet is automatically added from ../../python/read-format-file/ini/ini.py -->
```py
import configparser

config = configparser.ConfigParser()
# also "write" method exists
config.read("example.properties")

print(config.sections())
print(config["remote"]["another-value"])
print(config["without-section-property"])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## json

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/read-format-file/json/json.py) -->
<!-- The below code snippet is automatically added from ../../python/read-format-file/json/json.py -->
```py
import json
from pprint import pprint

with open('example.json') as f:
    data = json.load(f)

# for unix don't do this:
# data = json.load(open('example.json'))

pprint(data)

print(data["maps"][0]["id"])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## properties

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/read-format-file/properties/properties.py) -->
<!-- The below code snippet is automatically added from ../../python/read-format-file/properties/properties.py -->
```py
from jproperties import Properties
# only for Python2

p = Properties()
with open("example.properties", "r") as f:
    p.load(f, "utf-8")
print(p["property1"])
print(p["property2"])
print(p["another-value"])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## properties

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/read-format-file/properties/properties2.py) -->
<!-- The below code snippet is automatically added from ../../python/read-format-file/properties/properties2.py -->
```py
from jproperties import Properties

p = Properties()
with open("example.properties", "r") as f:
    p.load(f, "utf-8")
print(p["property1"])
print(p["property2"])
print(p["another-value"])



# Python3 example
import configparser
parser = configparser.RawConfigParser(default_section="default")
parser.read(path_to_settings_file)
return (parser.get("default", "template"), parser.get("default", "cv"))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## txt

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/read-format-file/txt/read-txt-file.py) -->
<!-- The below code snippet is automatically added from ../../python/read-format-file/txt/read-txt-file.py -->
```py
import sys

if __name__=='__main__':
    with open(sys.argv[1], "r") as file:
        for each_line in file:
            word1, word2 = each_line.split(" ")[:2]
            print(word1, word2.strip())
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## xml

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/read-format-file/xml/xml-dom-read.py) -->
<!-- The below code snippet is automatically added from ../../python/read-format-file/xml/xml-dom-read.py -->
```py
from xml.dom import minidom

xmldoc = minidom.parse('example.xml')

itemlist = xmldoc.getElementsByTagName('item')
print(len(itemlist))
print(itemlist[0].attributes['name'].value)

for s in itemlist:
    print(s.attributes['name'].value)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## xml

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/read-format-file/xml/xml-read.py) -->
<!-- The below code snippet is automatically added from ../../python/read-format-file/xml/xml-read.py -->
```py
import xmltodict

with open('example.xml') as fd:
    doc = xmltodict.parse(fd.read())

print(doc["data"]["items"]["@size"]) 
print(doc["data"]["items"]["item"][2])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## xml

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/read-format-file/xml/xml-sax-read.py) -->
<!-- The below code snippet is automatically added from ../../python/read-format-file/xml/xml-sax-read.py -->
```py
import xml.sax

# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# override the default ContextHandler
# Handler = MovieHandler()
# parser.setContentHandler( Handler )

class Handler(xml.sax.ContentHandler):
	def __init__(self):
		print("__init__")

	def startElement(self, tag, attributes):
		print("start-tag: %s attributes: %s " % (tag, attributes))

	def endElement(self, tag):
		print(" end -tag %s " % (tag))

	def characters(self, content):
		print(" content : " + content)


parser.setContentHandler(Handler())
xml_object = parser.parse("example.xml")
print(xml_object)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## yaml

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/read-format-file/yaml/yaml-read.py) -->
<!-- The below code snippet is automatically added from ../../python/read-format-file/yaml/yaml-read.py -->
```py
# pip search yaml
# pip install pyyaml
import yaml

with open("example.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

print(cfg['mysql']['password'])
```
<!-- MARKDOWN-AUTO-DOCS:END -->


