import sys


def main():
    for each_line in sys.stdin:
        words = each_line.strip().split("\t")
        count = words[0]
        for letter in  words[1].strip().split(","):
            print(count+","+letter+"\t1") 

if __name__ == '__main__':
    main()