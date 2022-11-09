# datetime

## datetime log parser

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/datetime/datetime-log-parser.py) -->
<!-- The below code snippet is automatically added from ../../python/datetime/datetime-log-parser.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## t time2timestamp

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/datetime/t-time2timestamp.py) -->
<!-- The below code snippet is automatically added from ../../python/datetime/t-time2timestamp.py -->
```py
import time
# T-timestamp to date 
datestr = "20211214T112448" +" GMT"
print(int(time.mktime(time.strptime(datestr, "%Y%m%dT%H%M%S %Z"))))
# date -d @1639477488
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## timestamp

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/datetime/timestamp.py) -->
<!-- The below code snippet is automatically added from ../../python/datetime/timestamp.py -->
```py
#!/usr/bin/env python
import datetime
import sys
# expected input: 1558082585167
d=datetime.datetime.fromtimestamp(int(sys.argv[1])/1000);print(str(d.day)+"."+str(d.month)+"."+str(d.year)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second))
```
<!-- MARKDOWN-AUTO-DOCS:END -->


