import sys


def main():
    for each_line in sys.stdin:
        words = each_line.strip().split(",")
        print(words[1]+"\t1")

if __name__ == '__main__':
    main()