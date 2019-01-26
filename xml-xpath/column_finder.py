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
