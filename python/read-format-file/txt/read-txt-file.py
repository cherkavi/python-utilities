import sys

if __name__=='__main__':
    with open(sys.argv[1], "r") as file:
        for each_line in file:
            word1, word2 = each_line.split(" ")[:2]
            print(word1, word2.strip())