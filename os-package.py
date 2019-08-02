#!/usr/bin/env python

# example to send signal to current process.

import os
import signal
import sys
import syslog
import time

# send signal to current process
signal.signal(signal.SIGHUP, signal.SIG_IGN)


class SignalListener:
    """
    listen shutdown signal from Operation System
    """
    def __init__(self):
        self.shutdown = False
        signal.signal(signal.SIGINT, self._process_shutdown)
        signal.signal(signal.SIGTERM, self._process_shutdown)

    def _process_shutdown(self, signum, frame):
        self.shutdown = True
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("shutdown !!! ")
        

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
