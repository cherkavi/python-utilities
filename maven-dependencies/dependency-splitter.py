import sys


if __name__ == '__main__':
    file_counter = 0
    file_output = None

    for each_line in sys.stdin:
        if each_line.find("---<") > 0:
            if file_output:
                file_output.close()
                file_output = None
                continue

        if each_line.find("@") > 0 and each_line.find("---"):
            file_counter = file_counter + 1
            file_output = open("%s.log" % str(file_counter).zfill(3), "w")
            continue

        if file_output and each_line.startswith("[INFO] "):
            print(each_line, end='', file=file_output)
