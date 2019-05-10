#!/usr/bin/env python3
import sys
from lxml import etree


class Path:

    def __init__(self, xml_element):
        self.id=xml_element.attrib["id"]
        self.style=Path.parse_style(xml_element.attrib["style"])
        self.d=Path.parse_path(xml_element.attrib["d"])

    def __str__(self):
        return "style: "+str(self.style)+"\nd: "+str(self.d)

    @staticmethod
    def parse_style(svg_style):
        # dictionary from string with delimiters 
        return dict( (key, value) for key,value in (each.split(":") for each in  svg_style.split(";") ))

    @staticmethod
    def parse_path(path):
        return dict( (float(x),float(y)) for x,y in (each.split(',') for each in path.split(" ")[1:])  )


def read_file(path_to_file):
    xml_parser = etree.XMLParser(recover=True, no_network=True, dtd_validation=False, load_dtd=False)
    root_element = etree.parse(path_to_file, xml_parser).getroot()
    # xpath with namespaces
    ns = {"svg": "http://www.w3.org/2000/svg"}
    for each in root_element.xpath('//svg:path', namespaces=ns):
         print(Path(each))



if __name__=="__main__":
    read_file(sys.argv[1])

# ./interpolation.py red-line.svg
