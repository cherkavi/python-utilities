# xml-xpath

## column_finder

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/xml-xpath/column_finder.py) -->
<!-- The below code snippet is automatically added from ../../python/xml-xpath/column_finder.py -->
```py
from lxml import etree
import argparse
import logging
import os
import column_mapper


def unknown_column_exists(root_element):
    """ find not existing columns """
    result = set()
    for each in root_element.xpath(
            '/SessionData/Protocol/TestModule[6]/ModuleStep[6]/SubModule/ModuleStep/SubModule/ModuleStep[3]/Action/UiDialog/MessageText/Text'):
        text = each.text
        index_begin = text.find('[#') + 2
        index_end = text.index('#]')
        if index_begin < 0 or index_end < 0:
            raise IndexError("index_begin = %s  index_end = %s " % (index_begin, index_end))
        for each_column in text[index_begin:index_end].split("#"):
            each_column = each_column.strip().lower()
            if each_column not in column_mapper.columns:
                result.add(each_column)
    return result


xml_parser = etree.XMLParser(recover=True, no_network=True, dtd_validation=False, load_dtd=False)


def parse_file(path_to_file):
    root = etree.parse(path_to_file, xml_parser)
    new_columns = unknown_column_exists(root)
    if len(new_columns) > 0:
        return new_columns
    else:
        return set()


def main(source_folder, file_extension, error_folder, target_folder):
    result = set()
    for each_file in os.listdir(source_folder):
        path_to_file = os.path.join(source_folder, each_file)
        if each_file.endswith(file_extension):
            logging.info("processing file: " + each_file)
            try:
                new_columns = parse_file(path_to_file)
            except IndexError:
                logging(" wrong XML format for file: "+each_file)
                column_mapper.move_file(path_to_file, error_folder)
                continue
            if len(new_columns) > 0:
                logging.info("new columns were found into file: " + each_file)
                result = result.union(new_columns)
                column_mapper.move_file(path_to_file, error_folder)
        else:
            logging.info("unknown file extension: " + each_file)
        column_mapper.move_file(path_to_file, target_folder)
    for each_new_column in result:
        print(' "%s": "m000", ' % (each_new_column, ))


# --sourceFolder /home/technik/projects/temp/zip-tester/source --targetFileExtension .behdat --errorFolder /home/technik/projects/temp/zip-tester/destination --targetFolder /home/technik/projects/temp/zip-tester/processed
if __name__ == "__main__":
    app_description = """ parse xml files and find columns, that not exists into [column_mapper.py - Storage mapping]
    errorFolder will contains XML files with unknown data
    targetFolder will contains XML files with already known column 
    """

    argument_parser = argparse.ArgumentParser(description=app_description)

    argument_parser.add_argument('--sourceFolder',
                                 help='folder with xml files',
                                 required=True)
    argument_parser.add_argument('--targetFileExtension',
                                 help='extension for files that will considered as xml',
                                 required=True)
    argument_parser.add_argument('--errorFolder'
                                 , help="errorFolder folder will contains files with unknown columns"
                                 , required=True)
    argument_parser.add_argument('--targetFolder'
                                 , help="folders for processed files, default behaviour - remove them"
                                 , required=False
                                 , default=None)
    args = argument_parser.parse_args()
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)
    main(args.sourceFolder, args.targetFileExtension, args.errorFolder, args.targetFolder)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## column_mapper

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/xml-xpath/column_mapper.py) -->
<!-- The below code snippet is automatically added from ../../python/xml-xpath/column_mapper.py -->
```py
import os

"""
map columns from XML file ( Text element ) to Storage fields
"""
columns = {
    "coolant temperature": "m001",
    "vehicle speed": "m002",
    "gear": "m003",
    "accelerator pedal position": "m004",
    "engine speed": "m005",
    "throttle valve position": "m006",
    "charge air pressure": "m007",
    "intake air temperature": "m008",
    "rail pressure": "m009",
    "ambient pressure": "m010",
    "fuel temperature": "m011",
    "lambda signal before catalytic converter": "m012",
    "status synchronisation camshaft-crankshaft": "m013",
    "operating mode": "m014",
    "engine status": "m015",
    "actuation rate wastegate": "m016",
    "rough running cylinder 1": "m017",
    "rough running cylinder 2": "m018",
    "rough running cylinder 3": "m019",
    "rough running cylinder 4": "m020",
    "rough running cylinder 5": "m021",
    "rough running cylinder 6": "m022",
    "rough running cylinder 7": "m023",
    "rough running cylinder 8": "m024",
    "rough running cylinder 9": "m025",
    "rough running cylinder 10": "m026",
    "rough running cylinder 11": "m027",
    "rough running cylinder 12": "m028",
    "misfire cylinder 1": "m029",
    "misfire cylinder 2": "m030",
    "misfire cylinder 3": "m031",
    "misfire cylinder 4": "m032",
    "misfire cylinder 5": "m033",
    "misfire cylinder 6": "m034",
    "misfire cylinder 7": "m035",
    "misfire cylinder 8": "m036",
    "misfire cylinder 9": "m037",
    "misfire cylinder 10": "m038",
    "misfire cylinder 11": "m039",
    "misfire cylinder 12": "m040",
    "combustion period cylinder 1": "m041",
    "combustion period cylinder 2": "m042",
    "combustion period cylinder 3": "m043",
    "combustion period cylinder 4": "m044",
    "combustion period cylinder 5": "m045",
    "combustion period cylinder 6": "m046",
    "combustion period cylinder 5": "m047",
    "combustion period cylinder 6": "m048",
    "combustion period cylinder 7": "m049",
    "combustion period cylinder 8": "m050",
    "combustion period cylinder 7": "m051",
    "combustion period cylinder 8": "m052",
    "combustion period cylinder 9": "m053",
    "combustion period cylinder 10": "m054",
    "combustion period cylinder 11": "m055",
    "combustion period cylinder 12": "m056",
    "oil temperature": "m057",
    "ambient temperature": "m058",
    "setpoint rail pressure": "m059",
    "setpoint fuel delivery period of quantity control valve": "m060",
    "fuel delivery period of quantity control valve": "m061",
    "duty cycle fuel pump control electronics": "m062",
    "faultbit fuel pump control electronics": "m063",
    "fuel tank level right": "m064",
    "fuel tank level left": "m065",
    "fuel tank level": "m066",
    "differential pressure gasoline particulate filter": "m067",
    "exhaust temperature befor gasoline particulate filter": "m068",
    "exhaust temperature befor gasoline particulate filter 2": "m069",
    "exhaust temperature in gasoline particulate filter": "m070",
    "exhaust temperature in gasoline particulate filter 2": "m071",
    "carbon black mass in gasoline particulate filter": "m072",
    "carbon black mass in gasoline particulate filter 2": "m073",
    "carbon black mass and soot load in gasoline particulate filter 2": "m074",
    "differential pressure gasoline particulate filter 2": "m075"
}


def column_by_value(find_value):
    if find_value == 'time':
        return "time"
    for key, value in columns.items():
        if value == find_value:
            return key
    return None


def move_file(source_file, folder):
    """ move file from [source_file] to [folder] """
    if folder:
        file = os.path.join(folder, os.path.basename(source_file))
        if os.path.exists(source_file):
            os.rename(source_file, file)
    else:
        os.remove(source_file)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## svg parse

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/xml-xpath/svg-parse.py) -->
<!-- The below code snippet is automatically added from ../../python/xml-xpath/svg-parse.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## xml2json

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/xml-xpath/xml2json.py) -->
<!-- The below code snippet is automatically added from ../../python/xml-xpath/xml2json.py -->
```py
import argparse
import logging
import os
import column_mapper
import random
# https://lxml.de/installation.html
from lxml import etree
import json


xml_parser = etree.XMLParser(recover=True, no_network=True, dtd_validation=False, load_dtd=False)


def read_file_meta_data(root_element):
    """ read meta data for all Text blocks """
    return_value = {}
    for each in root_element.xpath('/SessionData/Header/SessionInfo/*'):
        return_value[each.tag] = each.text
    session_info = root_element.xpath('/SessionData/Header/SessionInfo')[0]
    return_value["StartTime"] = session_info.get("StartTime")
    return_value["EndTime"] = session_info.get("EndTime")
    return return_value


def read_block_meta_data(text_element):
    """ meta data for certain block  """
    start_time = text_element.getparent().getparent().getparent().get('StartTime')
    end_time = text_element.getparent().getparent().getparent().get('EndTime')
    return {"BlockStartTime": start_time, "BlockEndTime": end_time}


def get_column(text, path_to_file):
    index_begin = text.find('[#') + 2
    index_end = text.find('#]')
    if index_begin < 0 or index_end < 0:
        raise RuntimeError("for file %s is impossible to parse columns block for table data with delimiters "
                           "'[#' and '#]' index_begin = %s  index_end = %s " % (path_to_file, index_begin, index_end))
    return list(map(lambda x: column_mapper.columns[x.strip().lower()], text[index_begin:index_end].split("#")))


def get_data(text, path_to_file):
    """ from text element parse data """
    index_begin = text.find('#]') + 2
    index_end = text.find("#&lt;/span", index_begin)
    if index_end < 0:
        index_end = text.find("</span", index_begin)
    if index_begin < 0 or index_end < 0:
        raise RuntimeError("for file %s is impossible to parse Text block for table data "
                           "with delimiters '#]' and '</span' " % (path_to_file, ))
    return list(map(lambda x: x.strip(), text[index_begin: index_end].split("#")))


def data_row(columns, row):
    return_value = dict()
    return_value["time"] = float(row[0].replace(",", "."))
    for index in range(1, len(columns)):
        return_value[columns[index-1]] = float(row[index].replace(",", "."))
    return return_value


def data_to_dict(columns, data):
    return_value = list()
    for row in data:
        row = row.strip()
        if len(row) == 0:
            continue
        elements = row.split(";")
        if len(elements) < 19:
            logging.error("data skew: "+row)
            continue
        return_value.append(data_row(columns, elements))
    return return_value


def digits_only(value):
    return ''.join(ch for ch in value if ch.isdigit())


def save_file(file_name, destination_folder, data):
    with open(os.path.join(destination_folder, file_name), "w") as output_file:
        output_file.write(json.dumps(data))


def create_json(meta_data, data, destination_folder):
    file_name = digits_only(meta_data["BlockStartTime"]) \
                + "-" \
                + digits_only(meta_data["BlockEndTime"]) \
                + "-" \
                + str(random.randint(100, 999)) \
                + ".json"
    logging.info("new json file created: " + file_name)
    save_file(file_name, destination_folder, {
                 "MetaData": meta_data,
                 "Data": data
             })


def process_xml(path_to_file, destination_folder):
    root_element = etree.parse(path_to_file, xml_parser)
    counter = 0
    for each in root_element.xpath(
            '/SessionData/Protocol/TestModule/ModuleStep[6]/SubModule/ModuleStep/SubModule/ModuleStep[3]/Action/UiDialog/MessageText/Text'):
        text = each.text
        if text.find("#]0,000;") < 0:
            continue
        counter = counter+1
        # todo - why data is duplicated - removed by next script with calculating md5sum?
        # if counter % 2 == 0:
        #    continue
        meta_data = read_file_meta_data(root_element)
        meta_data.update(read_block_meta_data(each))
        columns = get_column(text, path_to_file)
        meta_data["BlockColumns"] = columns
        create_json(meta_data,
                    data_to_dict(columns, get_data(text, path_to_file)),
                    destination_folder)
    return counter


def main(source_folder, file_extension, destination_folder, processed_folder, error_folder):
    for each_file in os.listdir(source_folder):
        source_file = os.path.join(source_folder, each_file)
        if each_file.endswith(file_extension):
            logging.info("processing file: " + each_file)
            try:
                counter = process_xml(source_file, destination_folder)
                if counter > 0:
                    column_mapper.move_file(source_file, processed_folder)
                else:
                    logging.error("no Text blocks found in file :" + source_file)
                    column_mapper.move_file(source_file, error_folder)
            except RuntimeError as ex:
                logging.error("can't parse file: %s  error is: %s " % (source_file, ex.args[0]))
                column_mapper.move_file(source_file, error_folder)
        else:
            logging.info("unknown file extension: " + each_file)
            column_mapper.move_file(source_file, error_folder)


# --sourceFolder /home/technik/projects/temp/zip-tester/source --targetFileExtension .behdat --destinationFolder /home/technik/projects/temp/zip-tester/destination --errorFolder /home/technik/projects/temp/zip-tester/error --processedFolder /home/technik/projects/temp/zip-tester/processed
if __name__ == "__main__":
    app_description = """ 
    application to parse XML file and copy results to json file - for writing them into Mongo
    sourceFolder - source of XML
    destinationFolder - output of script
    errorFolder - for wrong/broken files
    processedFolder - move/remove processed files"""

    parser = argparse.ArgumentParser(description=app_description)

    parser.add_argument('--sourceFolder'
                        , help='folder with xml files'
                        , required=True)
    parser.add_argument('--targetFileExtension'
                        , help='extension for files that will considered as xml'
                        , required=True)
    parser.add_argument('--destinationFolder'
                        , help="destination folder for results"
                        , required=True)
    parser.add_argument('--errorFolder'
                        , help="error folder for wrong file format, data skew"
                        , required=True)
    parser.add_argument('--processedFolder'
                        , help="folders for processed files, default behaviour - remove them"
                        , required=False
                        , default=None)
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)
    main(args.sourceFolder, args.targetFileExtension, args.destinationFolder, args.processedFolder, args.errorFolder)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


