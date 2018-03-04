import sys
import os

def read_tail(file_path, length):
    return_value = list()
    with open(file_path) as data_file:
        for line in data_file:
            return_value.append(line)
            if len(return_value) > length:
                return_value.pop(0)
    return return_value

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print ( "need to specify input file" )
        sys.exit(1)

    file_name = sys.argv[1]
    if not os.path.isfile(file_name):
        raise Exception("file was not found: "+file_name)

    for each_line in read_tail(file_name, 5):
        print each_line[:-1]
