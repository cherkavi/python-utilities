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