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
