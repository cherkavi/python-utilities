import sys

def main():
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") if len(each.strip())>0 ]
        print(values[2])

if __name__ == '__main__':
    main()