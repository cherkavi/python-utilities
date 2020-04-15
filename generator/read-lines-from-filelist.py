import sys

def read_lines(list_of_files):
    def _read_lines():
        for each_file in list_of_files:
            with open(each_file) as current_file:
                yield from current_file
    yield from enumerate(_read_lines())

if __name__ == "__main__":
    for each_line in read_lines(sys.argv[1:]):
        print(each_line)

