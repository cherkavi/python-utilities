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
