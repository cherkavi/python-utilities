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