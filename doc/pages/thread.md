# thread

## function in thread

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/thread/function-in-thread.py) -->
<!-- The below code snippet is automatically added from ../../python/thread/function-in-thread.py -->
```py
from multiprocessing import Process
from time import sleep

def long_time_processing(prefix:str, amount_of_iteration:int):
    for index in range(amount_of_iteration):
        print(prefix, index)
        sleep(0.3)

if __name__=="__main__":
    # start Thread from function, function thread
    Process(target=long_time_processing, args=("first ", 8)).start()
    sleep(1)
    Process(target=long_time_processing, args=("second ", 5)).start()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## thread

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/thread/thread.py) -->
<!-- The below code snippet is automatically added from ../../python/thread/thread.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->


