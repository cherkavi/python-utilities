#!/usr/bin/env python

# example to send signal to current process.

import os
import signal
import sys
import syslog
import time

# send signal to current process
signal.signal(signal.SIGHUP, signal.SIG_IGN)

# pid id of current process
os.getpid()

# pid of parent process
os.getppid()

# run child process
os.spawnv(os.P_WAIT, path, args)

# execute external program with replacing current process
os.execv(to_launch[0], to_launch)

# write data into syslog 
syslog.syslog(syslog.LOG_ERR, str(sys.exc_info()))
