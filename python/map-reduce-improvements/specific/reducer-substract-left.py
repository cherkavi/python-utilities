import sys

def main():
    last_key = None
    last_letter = None
    printed = False
    last_line = None
    for line in sys.stdin:
        if line == last_line:
            continue
        values = [each.strip() for each in line.split("\t") ]
        key = values[0]
        letter = values[1]
        
        if last_key != key:
            if last_letter!=letter:
                print(key)
                printed = True
        else:
            printed = False
        last_key = key
        last_letter = letter
        last_line = line
    if not printed and last_letter=='A':
        print(key)

if __name__ == '__main__':
    main()