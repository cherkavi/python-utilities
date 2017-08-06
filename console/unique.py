import sys

def main(arguments) :
    if len(arguments) == 0:
        print("name of file should be specified")
        sys.exit(1)
    unique_lines = set()
    with open(arguments[0]) as f:
        for line in f:
            unique_lines.add(line)
    for eachLine in unique_lines:
        print(eachLine[:-1])

if __name__ == "__main__":
    main(sys.argv[1:])

