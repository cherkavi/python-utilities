#!/usr/bin/env python
import datetime
import sys
# expected input: 1558082585167
d=datetime.datetime.fromtimestamp(int(sys.argv[1])/1000);print(str(d.day)+"."+str(d.month)+"."+str(d.year)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second))
