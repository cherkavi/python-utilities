import sys

def main():
    last_key = None
    count = 0
    size = 0

    def print_values():
        print(last_key + "\t" + str(int(size/count)))

    for each_line in sys.stdin:
        key_value = each_line.strip().split("\t")
        if len(key_value)<2:
            continue
        key = key_value[0]
        value = key_value[1]

        if key!=last_key:
            if last_key:
                print_values()
            count=1
            size = int(value)
            last_key = key
        else:
            count+=1
            size = size+int(value)

    print_values()



if __name__ == '__main__':
    main()