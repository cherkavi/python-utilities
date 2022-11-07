#!/usr/bin/env python3
import sys
from lxml import etree
import random



class Path:
    """
    represent a element from xml 
    """
    def __init__(self, xml_element):
        # xml attribute, xml read attribute
        self.id=xml_element.attrib["id"]
        self.style=Path._parse_style(xml_element.attrib["style"])
        self.d=Path._parse_path(xml_element.attrib["d"])

    def __str__(self):
        return "style: "+str(self.style)+"\nd: "+str(self.d)

    @staticmethod
    def _parse_style(svg_style):
        return dict( (key, value) for key,value in (each.split(":") for each in  svg_style.split(";") ))

    @staticmethod
    def _parse_path(path):
        return dict( (float(x),float(y)) for x,y in (each.split(',') for each in path.split(" ")[1:])  )

    @staticmethod
    def _to_d(list_of_tuples):
        """ convert list of pairs (tuples) to string representation for xml attribute in svg file """
        value = "M"
        for each in (" "+str(x)+","+str(y) for x,y in (each_pair for each_pair in list_of_tuples) ):
            value = value + each
        return value

    @staticmethod
    def to_path(list_of_tuples, color="ff0000"):
        """ print xml element to console """
        print("<path")
        print('  id="path'+str(random.randint(50000, 99999))+'"')
        print('  d="'+Path._to_d(list_of_tuples)+'"')
        print('  style="fill:none;stroke:#'+color+';stroke-width:0.26499999;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:0.26499999,0.79499996;stroke-dashoffset:0"')
        print ("/>")

    @staticmethod
    def create_element(xml_root, list_of_tuples, x, y, text, color="ff0000"):
        """ create xml sub-element in xml element """
        etree.SubElement(xml_root, 'path',
         id='path'+str(random.randint(50000, 99999)),
         d=Path._to_d(list_of_tuples),
         style="fill:none;stroke:#"+color+";stroke-width:0.26499999;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:0.26499999,0.79499996;stroke-dashoffset:0"
         )
        text_element = etree.SubElement(xml_root, 'text', style="font-style:normal;font-weight:normal;font-size:10.0px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.25", x=str(x), y=str(y), id='text'+str(random.randint(50000, 99999)))
        tspan = etree.SubElement(text_element, 'tspan', x=str(x), y=str(y), id='tspan'+str(random.randint(50000, 99999)), style="stroke-width:0.26458332;font-size:4.58611111px;fill:#"+color)         
        tspan.text=text


class Math:
    @staticmethod
    def interpolation_lagrang(original_positions, x_value):
        xData = list(original_positions.keys())
        yData = list(original_positions.values())
        result = 0
        for i in range(len(xData)):
            tmp = 1.0
            for j in range(len(xData)):
                if i != j:
                    tmp *= (x_value - xData[j]) / (xData[i] - xData[j])
            result += tmp * yData[i]
        return result        


    @staticmethod
    def interpolation_newton(original_positions, x_value):
        xData = list(original_positions.keys())
        yData = list(original_positions.values())

        result = 0
        for i in range (0, len(xData)):
            coef = 1
            for j in range(0, i):
                coef *= x_value-xData[j]
                
            dd = 0
            for j in range(0, i+1):
                g = 1
                for k in range(0, i+1):
                    if k != j:
                        g *= 1/(xData[j]-xData[k])
                dd += yData[j]*g
            result += coef*dd
    
        return result


    @staticmethod
    def interpolation(dict_values, interpolation_method, koef=10):
        x_current = min(dict_values.keys())
        x_end = max(dict_values.keys())
        step = float(x_end-x_current)/float(koef*len(dict_values))
        result = list()
        while(x_end>x_current):
            result.append( (x_current, interpolation_method(dict_values, x_current)) )
            x_current = x_current + step
        return result


def create_file(source_file, destination_file):
    xml_parser = etree.XMLParser(recover=True, no_network=True, dtd_validation=False, load_dtd=False)
    root_element = etree.parse(source_file, xml_parser).getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}
    xml_g_element = root_element.xpath('//svg:g', namespaces=ns)[0]
    for each in root_element.xpath('//svg:path', namespaces=ns):
        path = Path(each)
        Path.create_element(xml_g_element, Math.interpolation(path.d, interpolation_method=Math.interpolation_lagrang), min(path.d.keys()), max(path.d.values())+10, "lagrang", color="ffa000")
        Path.create_element(xml_g_element, Math.interpolation(path.d, interpolation_method=Math.interpolation_newton), min(path.d.keys()), max(path.d.values())+15, "newton", color="ff8000")
        # Path.to_path(Math.interpolation(path.d, interpolation_method=Math.interpolation_lagrang), color="ff0000")
        # Path.to_path(Math.interpolation(path.d, interpolation_method=Math.interpolation_newton), color="ff2000")
    # save xml to file
    etree.ElementTree(root_element).write(destination_file, xml_declaration=True, encoding='utf-8')
        


if __name__=="__main__":
    create_file(sys.argv[1], sys.argv[2])