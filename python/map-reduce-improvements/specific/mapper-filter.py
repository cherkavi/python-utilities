import sys

def main():
    for line in sys.stdin:
        values = [each.strip() for each in line.split("\t") if len(each.strip())>0 ]
        if values[1]=="user10":
            print("\t".join(values))

if __name__ == '__main__':
    main()