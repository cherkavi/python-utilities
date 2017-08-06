import sys
import threading
import time

class Worker(threading.Thread):
    def __init__(self, title):
        threading.Thread.__init__(self)
        self.title=title

    def run(self):
        for index in range(1,10):
            time.sleep(0.01)
            print(self.title+" "+str(index))

def main(arguments) :
    worker1=Worker("w1")
    worker2=Worker("w2")
    worker1.start()
    worker2.start()
    print("-- end --")


if __name__ == "__main__":
    main(sys.argv)

