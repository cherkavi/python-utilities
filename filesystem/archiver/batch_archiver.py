import shutil
import os
from datetime import datetime

class ImportFile:
    EXTENSION_SIZE = 4

    # expect to see string like: "Mobile_Tariff_2018_06_13_13_03.csv"
    def __init__(self, file_name):
        self.file_name = file_name
        self.suffix = file_name[-16-ImportFile.EXTENSION_SIZE:]                # '2018_06_13_13_03.xml'
        self.date = datetime.strptime(self.suffix[0:-ImportFile.EXTENSION_SIZE], "%Y_%m_%d_%H_%M")
        self.prefix = file_name[0:len(file_name)-len(self.suffix)]
        pass

    def __str__(self):
        return self.prefix+"   "+self.suffix


    @staticmethod
    def buckets(list_of_files):
        return_value = set()
        for each_file in list_of_files:
            return_value.add(each_file.prefix)
        return return_value

    @staticmethod
    def files_by_bucket(list_of_files, bucket_name):
        return sorted(filter(lambda x: x.prefix == bucket_name, list_of_files), key=lambda f: f.date, reverse=True)


class Logger:

    def __init__(self, path_to_file):
        self.out = open(path_to_file, "a")

    def write(self, message):
        self.out.write(message)
        self.out.write("\n")
        self.out.flush()

    def __del__(self):
        self.out.close()


def standard_archiving(files_in_bucket, source_folder, destination_folder):
    if len(files_in_bucket) < 2:
        return

    for each_file in files_in_bucket[1:]:
        path_to_file = os.path.join(source_folder, each_file.file_name)
        logger.write("move file: "+path_to_file)
        shutil.move(path_to_file, destination_folder)


def archive(source_folder, destination_folder, archive_function):
    import_files = [ImportFile(each_file) for each_file in os.listdir(source_folder)]
    for each_bucket_name in ImportFile.buckets(import_files):
        archive_function(ImportFile.files_by_bucket(import_files, each_bucket_name), source_folder, destination_folder)


if __name__ == '__main__':
    archive_folder = "archive"
    root_folder = "/home/technik/temp/import/"
    logger = Logger("/home/technik/temp/archive.txt")
    try:
        for each_folder in ["Mobile"]:
            archive(root_folder+each_folder, archive_folder, standard_archiving)
    finally:
        del logger
