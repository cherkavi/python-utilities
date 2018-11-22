import os
import subprocess

FNULL = open(os.devnull, 'w')
retcode = subprocess.call(['echo', 'foo'], stdout=FNULL, stderr=subprocess.STDOUT)

# It is effectively the same as running this shell command:
# retcode = os.system("echo 'foo' &> /dev/null")
