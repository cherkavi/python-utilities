import sys

def main():
    original_data = []
    
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") ]
        key = values[0]
        letter = values[1]

        if letter == 'A':
            if key not in original_data:
                original_data.append(key)
        else:
            if key in original_data:
                original_data.remove(key)
    for each in original_data:
        print(each)
if __name__ == '__main__':
    main()