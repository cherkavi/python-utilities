import sys

def main():
    last_key = None
    last_letter = None
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") ]
        key = values[0]
        letter = values[1]
        
        if last_key == key:
            if last_letter!=letter:
                print(key)

        last_key = key
        last_letter = letter

if __name__ == '__main__':
    main()