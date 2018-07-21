import sys

def main():
    last_value = None
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") ]
        value = values[0]
        if last_value!=value:
            if last_value:
                print(last_value)
            last_value = value
        print(last_value)

if __name__ == '__main__':
    main()