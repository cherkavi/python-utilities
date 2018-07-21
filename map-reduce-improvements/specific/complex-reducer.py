import sys


def main():
    previous_value = None
    for each_line in sys.stdin:
        words = each_line.strip().split("\t")
        if previous_value!=words[0]:
            if previous_value:
                print(previous_value)
        previous_value = words[0]
    print(previous_value)

if __name__ == '__main__':
    main()