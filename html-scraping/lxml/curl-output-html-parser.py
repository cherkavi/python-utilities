from lxml import html, etree
import sys

"""
read data from stdin, 
interpret it like full html text, 
print xpath from first command-line argument
usage example
```
curl -X GET google.com | python3 curl-output-html-parser.py "/html/head/title"
curl -X GET google.com | python3 curl-output-html-parser.py "/html/body/a/@href"
```
"""

# read all lines from stdin
lines = [each_line for each_line in sys.stdin]
# parse input data as html file
tree = html.fromstring("\n".join(lines))
if len(sys.argv)==0:
    elements = tree.xpath("/html")
else:
    elements = tree.xpath(sys.argv[1])
if len(elements)>0:
    # print( str(etree.tostring(elements[0])) )
    # print("".join([ str(child.text) for child in elements[0].iterdescendants()]))
    # print("".join([str(etree.tostring(child)) for child in elements[0].iterchildren()]))
    
    if hasattr(elements[0], "itertext"):
        print("\n".join([text.strip() for text in elements[0].itertext()]))
    else:
        print(elements[0])
    sys.exit(0)
else:
    sys.exit(1)
