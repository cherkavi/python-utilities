# ista

## soft

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ista/soft/json2mongo.py) -->
<!-- The below code snippet is automatically added from ../../python/ista/soft/json2mongo.py -->
```py
import argparse
import logging
import os
import column_mapper
import json
from pymongo import MongoClient


def process_json(path_to_file, mongo_collection):
    with open(path_to_file) as f:
        json_file = json.load(f)
    mongo_collection.insert_one(json_file)


def main(source_folder, processed_folder, error_folder, mongo_collection):
    for each_file in os.listdir(source_folder):
        source_file = os.path.join(source_folder, each_file)
        logging.info("processing file: " + each_file)
        try:
            process_json(source_file, mongo_collection)
            column_mapper.move_file(source_file, processed_folder)
        except RuntimeError as ex:
            logging.error("can't parse/write file: %s  error is: %s " % (source_file, ex.args[0]))
            column_mapper.move_file(source_file, error_folder)


# --sourceFolder /home/technik/projects/temp/zip-tester/source
# --processedFolder /home/technik/projects/temp/zip-tester/processed
# --errorFolder /home/technik/projects/temp/zip-tester/error
# --mongoUrl mongodb://localhost:27017/
# --mongoUser vitalii
# --mongoPassword vitalii
# --mongoDatabase ista-db
# --mongoCollection signals


if __name__ == "__main__":
    app_description = """ 
    read JSON files from Folder and insert them into MongoDB
    sourceFolder - source with JSON
    mongoUrl - url to mongo server, example "mongodb://localhost:27017/"
    mongoUser - user
    mongoPassword - password
    mongoDatabase - mongo db
    mongoCollection - collection     
    errorFolder - can't read JSON and write it into DB
    processedFolder - were successfully writen"""

    parser = argparse.ArgumentParser(description=app_description)

    parser.add_argument('--sourceFolder'
                        , help='source with JSON files'
                        , required=True)
    parser.add_argument('--processedFolder'
                        , help="folders with successfully written files"
                        , required=False)
    parser.add_argument('--errorFolder'
                        , help="error folder, files here when corrupted data or DB is not reachable "
                        , required=True)
    parser.add_argument('--mongoUrl'
                        , help="url to mongo server, example mongodb://localhost:27017/"
                        , required=True)
    parser.add_argument('--mongoUser'
                        , help="mongo user"
                        , required=True)
    parser.add_argument('--mongoPassword'
                        , help="mongo password"
                        , required=True)
    parser.add_argument('--mongoDatabase'
                        , help="mongo database"
                        , required=True)
    parser.add_argument('--mongoCollection'
                        , help="mongo collection"
                        , required=True)
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)

    mongoClient = MongoClient(args.mongoUrl, username=args.mongoUser, password=args.mongoPassword)
    mongoDb = mongoClient[args.mongoDatabase]
    mongoCollection = mongoDb[args.mongoCollection]

    main(args.sourceFolder,
         args.processedFolder,
         args.errorFolder,
         mongoCollection)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## soft

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ista/soft/md5-duplication-remover.py) -->
<!-- The below code snippet is automatically added from ../../python/ista/soft/md5-duplication-remover.py -->
```py
import logging
import os
import sys
import hashlib


def main(source_folder):
    file_list = dict()
    for each_file in os.listdir(source_folder):
        path_to_file = os.path.join(source_folder, each_file)
        with open(path_to_file, "r") as text_in_file:
            file_hash = hashlib.md5(text_in_file.read().encode("utf-8")).hexdigest()
        if file_hash in file_list:
            file_list[file_hash].append(path_to_file)
        else:
            file_list[file_hash] = [path_to_file]
    for key, value in file_list.items():
        value.pop(0)
        for each_redundant_file in value:
            os.remove(each_redundant_file)


if __name__ == "__main__":
    app_description = """ find duplication of context of files into folder
    ( calculate md5sum for all files )
    remove duplication
    """

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)

    if len(sys.argv) == 0:
        print("folder with files should be specified")
        sys.exit(1)
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print("specified path is not a folder:"+folder)
        sys.exit(2)
    main(folder)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## soft

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ista/soft/xml2json.py) -->
<!-- The below code snippet is automatically added from ../../python/ista/soft/xml2json.py -->
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



## soft

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ista/soft/zip-opener.py) -->
<!-- The below code snippet is automatically added from ../../python/ista/soft/zip-opener.py -->
```py
import zipfile
import os
import logging
import argparse


def move_processed_file(each_zip_file, destination_folder):
    if destination_folder:
        dest_zip_file = os.path.join(destination_folder, os.path.basename(each_zip_file))
        logging.info("processed file: "+dest_zip_file)
        os.rename(each_zip_file, dest_zip_file)
    else:
        os.remove(each_zip_file)


def extract_zip_file(zip_file, file_prefix, destination_folder):
    with zipfile.ZipFile(zip_file, 'r') as zipper:
        for file in zipper.namelist():
            if file.endswith(file_prefix):
                logging.info("new file:"+file)
                zipper.extract(file, destination_folder)


def main(zip_folder, file_prefix, destination_folder, processed_folder):
    for eachZipFile in os.listdir(zip_folder):
        path_to_zip_file=os.path.join(zip_folder, eachZipFile)
        if not zipfile.is_zipfile(path_to_zip_file):
            logging.info("not a zip file: "+eachZipFile)
        else:
            logging.info("extract zip file:"+eachZipFile)
            extract_zip_file(path_to_zip_file, file_prefix, destination_folder)
        move_processed_file(path_to_zip_file, processed_folder)


# --sourceFolder /home/technik/projects/temp/zip-tester/source --targetFileExtension .behdat --destinationFolder /home/technik/projects/temp/zip-tester/destination --processedFolder /home/technik/projects/temp/zip-tester/processed
if __name__ == "__main__":
    app_description = """ 
    application to read ZIP files from source folder
    retrieve from each of them file by mask
    move retrieved file to another folder, and remote/move processed file """

    parser = argparse.ArgumentParser(description=app_description)

    parser.add_argument('--sourceFolder',
                        help='folder with zip files',
                        required=True)
    parser.add_argument('--targetFileExtension',
                        help='extension for files that will be retrieved and moved',
                        required=True)
    parser.add_argument('--destinationFolder'
                        , help="destination forlder for found files"
                        , required=True)
    parser.add_argument('--processedFolder'
                        , help="folders for processed files, default behaviour - remove them"
                        , required=False
                        , default=None)
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)
    main(args.sourceFolder, args.targetFileExtension, args.destinationFolder, args.processedFolder)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


