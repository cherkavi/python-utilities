# xml-minidom

## read xml2

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/xml-minidom/read-xml2.py) -->
<!-- The below code snippet is automatically added from ../../python/xml-minidom/read-xml2.py -->
```py
from xml.dom.minidom import parse, parseString

dom = parse('ingest-pipeline.archimate')  # parse an XML file by name
components = [each_element for each_element in dom.getElementsByTagName("element") if each_element.getAttribute("xsi:type")=="archimate:ApplicationComponent" and each_element.hasChildNodes()]
# filter element by classtype, java "instance of" with shortName
component_description = list(map( lambda x:(x.getAttribute("name"), " ".join([each_child.firstChild.nodeValue for each_child in x.childNodes if each_child.__class__.__name__=="Element" and each_child.tagName=="documentation"])),components))
print(component_description)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


