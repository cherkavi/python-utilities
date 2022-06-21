import time
# T-timestamp to date 
datestr = "20211214T112448" +" GMT"
print(int(time.mktime(time.strptime(datestr, "%Y%m%dT%H%M%S %Z"))))
# date -d @1639477488
