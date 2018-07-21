import sys


def print_outer_join(values):
    for i in range(len(values)):
        for j in range(len(values)):
            if i!=j and values[i]!=values[j]:
                print(values[i]+","+values[j]+"\t1")

def main():
    for each_line in sys.stdin:
        words = each_line.strip().split(" ")
        print_outer_join(words)

if __name__ == '__main__':
    main()