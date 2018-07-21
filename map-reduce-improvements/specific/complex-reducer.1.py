import sys

def add_to_dictionary(values, letter, count):
    if letter in values:
        values[letter] = values[letter] + int(count)
    else:
        values[letter] = int(count)

def print_dictionary(values):
    for key, value in values.items():
        print(key+"\t"+str(value))


def main():
    values = dict()
    previous_line = None
    for each_line in sys.stdin:
        if previous_line==each_line:
            continue
        words = each_line.strip().split("\t")
        letter = words[1]
        add_to_dictionary(values, letter, 1)
        previous_line = each_line

    print_dictionary(values)

if __name__ == '__main__':
    main()