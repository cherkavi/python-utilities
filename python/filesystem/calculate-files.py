'''
calculate amount of files inside folder
'''
import sys
import os
import time
import datetime

def main(argv):
    while True:
        dt = datetime.datetime.fromtimestamp(time.time())
        print ( dt.strftime('%Y-%m-%dT%H:%M:%S'), "   ",  len(os.listdir(argv[0])) )
        time.sleep(1)

if __name__ == "__main__":
   main(sys.argv[1:])