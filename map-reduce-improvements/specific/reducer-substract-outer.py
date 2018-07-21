import sys

def main():
    original_data = []
    last_line = None
    for line in sys.stdin:
        if last_line == line:
            continue
        values = [each.strip() for each in line.split("\t") ]
        key = values[0]
        letter = values[1]

        if key in original_data:
            original_data.remove(key)
        else:
            original_data.append(key)
        last_line = line
    for each in original_data:
        print(each)
if __name__ == '__main__':
    main()