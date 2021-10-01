import sys, os, json

if __name__=='__main__':
    print("hello from pex")
    if len(sys.argv)>1:
        print(f"attempt to read json file: {sys.argv[1]}")
        with open(sys.argv[1], "r") as json_file:
            print(json.load(json_file))
