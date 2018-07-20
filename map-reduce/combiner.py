import sys

def main():
    last_key = None
    count = 0
    size = 0

    def print_values():
        print(last_key + "\t" + str(size)+";"+str(count))

    for each_line in sys.stdin:
        key_value = each_line.strip().split("\t")
        if len(key_value)<2:
            continue
        key = key_value[0]
        size_count = key_value[1].split(";")
        key_size = int(size_count[0])
        key_count = int(size_count[1])

        if key!=last_key:
            if last_key:
                print_values()
            count = key_count
            size = key_size
            last_key = key
        else:
            count += key_count
            size = size+key_size

    print_values()



if __name__ == '__main__':
    main()