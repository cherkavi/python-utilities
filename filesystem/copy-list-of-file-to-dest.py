import sys
import os
import shutil


def main(path_to_list, destination_folder):
    """ copy list of file into destination folder
    :param path_to_list: text file with list of files
    :param destination_folder: full path to destination folder
    """
    with open(path_to_list) as input_file:
        for each_line in input_file:
            file_candidate = each_line.strip()
            if os.path.isfile(file_candidate):
                print("%s %s" % (destination_folder,file_candidate))
                shutil.copy(file_candidate, destination_folder)


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("input parameters should be: <text file with list of files to be copied> <destination folder>")
        exit(1)
    main(sys.argv[1], sys.argv[2])
