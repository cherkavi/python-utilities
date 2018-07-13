from datetime import datetime
from datetime import timedelta
import sys

t_str = "2018-01-18 14:35:52.583"
t_str2 = "2018-01-18 14:37:02.583"
t = datetime.strptime(t_str[:19], "%Y-%m-%d %H:%M:%S")
t2 = datetime.strptime(t_str2[:19], "%Y-%m-%d %H:%M:%S")

print(t)
print(t2)
if t2<(t+timedelta(seconds=30)):
    print("less than 30 seconds")
else:
    print("more than 30 seconds")
#datetime.datetime.now()
print(t.strftime("%H:%M:%S"))