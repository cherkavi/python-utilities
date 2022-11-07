'''
execute jar file
'''
import sys
import os
import subprocess

def main(argv):
    if len(argv) < 0:
        exit("need to specify the jar file ")
    # os.spawnl(os.P_DETACH, 'java -jar c:\\temp\\long-execution.jar')
    # os.spawnl(os.P_NOWAIT, 'java -jar c:\\temp\\long-execution.jar')
	# os.system('cmd /c java -jar c:\\temp\\long-execution.jar')
	# os.system('start /b java -jar c:\\temp\\long-execution.jar')
    # subprocess.call("java  -jar c:\\temp\\long-execution.jar")
    # subprocess.Popen("java -jar c:\\temp\\long-execution.jar")

if __name__ == "__main__":
   main(sys.argv[1:])