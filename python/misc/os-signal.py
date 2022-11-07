import os, sys
import time
import signal
def func(signum, frame):
    print 'You raised a SigInt! Signal handler called with signal', signum

signal.signal(signal.SIGINT, func)
while True:
    print "Running...",os.getpid()
    time.sleep(2)
    os.kill(os.getpid(),signal.SIGINT)


##############################################################

import signal  
import time  
 
# Our signal handler
def signal_handler(signum, frame):  
    print("Signal Number:", signum, " Frame: ", frame)  
 
def exit_handler(signum, frame):
    print('Exiting....')
    exit(0)
 
# Register our signal handler with `SIGINT`(CTRL + C)
signal.signal(signal.SIGINT, signal_handler)
 
# Register the exit handler with `SIGTSTP` (Ctrl + Z)
signal.signal(signal.SIGTSTP, exit_handler)


signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGILL, signal_handler)
signal.signal(signal.SIGTRAP, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)
signal.signal(signal.SIGBUS, signal_handler)
signal.signal(signal.SIGFPE, signal_handler)
#signal.signal(signal.SIGKILL, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGSEGV, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)
signal.signal(signal.SIGPIPE, signal_handler)
signal.signal(signal.SIGALRM, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# While Loop
while 1:  
    print("Press Ctrl + C") 
    time.sleep(3)


###########################################################
def register_signals(self) -> None:
        """Register signals that stop child processes"""
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)
        signal.signal(signal.SIGUSR2, self._debug_dump)

    def _exit_gracefully(self, signum, frame) -> None:
        sig_name = signal.Signals(signum).name
        
        """Helper method to clean up processor_agent to avoid leaving orphan processes."""
        if not _is_parent_process():
            # Only the parent process should perform the cleanup.
            return
