from time import sleep
from gevent.pool import Group
import gevent
import gevent.threadpool

def counter(name:str, size:int) -> None:
    for each in range(1,size):
        print(f" {name}: {each}")
        sleep(0.5)

# 
# group: Group=Group()
group: gevent.pool.Pool = gevent.get_hub().threadpool
group.spawn(counter, "thread-1", 10)
sleep(1)
group.spawn(counter, "thread-2", 10)
print("waiting for magic")
group.join()
print("end")




