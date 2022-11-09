# subprocess

## check file existence

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/subprocess/check-file-existence.py) -->
<!-- The below code snippet is automatically added from ../../python/subprocess/check-file-existence.py -->
```py
import subprocess
import os

FNULL = open(os.devnull, 'w')

try:
	value = subprocess.check_call(["ls","/data/store/collected/car-data/4f1a-a1b4-4bee05c9c281/MDF4/20181129T105009.MF4"], shell=False, stderr=FNULL, stdout=FNULL)
except Exception as e:
	print(e.returncode)
else:
	print("OK")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## check ip

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/subprocess/check-ip.py) -->
<!-- The below code snippet is automatically added from ../../python/subprocess/check-ip.py -->
```py
#!/usr/bin/env python
import subprocess

output = subprocess.check_output(["curl", "--silent", "https://api.ipify.org"])
print(output)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## curl

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/subprocess/curl.py) -->
<!-- The below code snippet is automatically added from ../../python/subprocess/curl.py -->
```py
import subprocess
import json
from typing import List

def clear_binary_line(b_line:bytes) -> str:
    # convert bytes to string, bytes2string, byte to string
    next_line = b_line.decode('utf-8')
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    index = next_line.rfind("/")
    if index >= 0:
        next_line = next_line[index+1:]
    return next_line

# subprocess curl, requests emulator, requests clear call
code="bx4pqba"
client_id="dj0yJmTBj"
client_secret="a871c009"
redirect_uri="https://ec2-5.eu-central-1.compute.amazonaws.com"
command=f"curl -X POST https://api.login.yahoo.com/oauth2/get_token --data 'code={code}&grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&response_type=code'"
output:bytes = subprocess.check_output(command.split(" "))
response: dict = json.loads(clear_binary_line(output))

if "error" in response:
    print(response["error"])
    print(response["error_description"])
else:
    print(response["access_token"])
    print(response["refresh_token"])
    print(response["expires_in"])
    print(response["bearer"])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## execute batch job

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/subprocess/execute-batch-job.py) -->
<!-- The below code snippet is automatically added from ../../python/subprocess/execute-batch-job.py -->
```py
#!/usr/bin/env python
'''
execute jar file
'''
import sys
import os
import subprocess
import string
import time
import datetime

EXEC_TIMES = 7
EXECUTED_LIST_FILE = "batch-result.txt"


black_list = ["C:/project/horus/horus-batch-deploy/target/horus-batch-deploy-8.29.0.RC1-SNAPSHOT/bin/account-snapshot-refresh.py"
,"C:/project/horus/horus-batch-deploy/target/horus-batch-deploy-8.29.0.RC1-SNAPSHOT/bin/balance-transfer-correction.py"
,"C:/project/horus/horus-batch-deploy/target/horus-batch-deploy-8.29.0.RC1-SNAPSHOT/bin/balas-migration.py"
]


def clear_binary_line(b_line):
    # convert bytes to string, bytes2string, byte to string
    next_line = b_line.decode('utf-8')
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    index = next_line.rfind("/")
    if index >= 0:
        next_line = next_line[index+1:]
    return next_line
    

def collect_files(argv):
    if len(argv) <= 0:
        exit("need to specify the jar file ")

    path = argv[0]
    path_to_scripts = path

    process = subprocess.Popen( ("ls %s*.py" % (path)).split(" "), stdout = subprocess.PIPE )

    list_of_files = []
    for line in process.stdout:
        list_of_files.append( os.path.join(path_to_scripts, clear_binary_line(line)) )
    process.stdout.close()
    return list_of_files


def execution_waiting_for_string(command, pattern):
    process = subprocess.Popen( command.split(" "), stdout = subprocess.PIPE )
    result = False
    for b_line in process.stdout:
        if result:
            continue
        line = clear_binary_line(b_line)
        print(">>> %s" % (line))
        if line.find(pattern) >= 0:
            result = True
    process.stdout.close()
    return result


def current_time():
     # return datetime.datetime.now()
     return time.time()*1000


def execute_script(script):
    print("start to execute script: %s" % (script) )
    return execution_waiting_for_string("python "+ script, "exiting with code 0")


def write_result(script, execution_time_ms):
    with open(EXECUTED_LIST_FILE, "a") as file:
        result_string = "script:%s   time:%f" % (script, execution_time_ms)
        print( result_string )
        file.write( result_string )
        file.write( "\n" )


if __name__ == "__main__":
    #list_of_scripts = collect_files(sys.argv[1:])
    list_of_scripts = ["C:/project/horus/horus-batch-deploy/target/horus-batch-deploy-8.29.0.RC1-SNAPSHOT/bin/bulk-account-creation.py",
                       ]

    for each_script in list_of_scripts:
        if str(each_script) in black_list:
            print("black list: %s" % each_script)
            continue
        for index in range(0, EXEC_TIMES):
            time_begin = current_time()
            exec_result = execute_script(each_script)
            time_end = current_time()

            if exec_result:
                write_result(each_script, time_end-time_begin)
            else:
                print("result is False for: %s" % (each_script))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## execute jar file

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/subprocess/execute-jar-file.py) -->
<!-- The below code snippet is automatically added from ../../python/subprocess/execute-jar-file.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## execute_line

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/subprocess/execute_line.py) -->
<!-- The below code snippet is automatically added from ../../python/subprocess/execute_line.py -->
```py
import sys
import subprocess
import os
import stat

def execute_line(command_line):
	file_name = "1.sh"
	out_file = "out.txt"
	with open(file_name, "w") as output:
		output.write(command_line+" > "+out_file)
	os.chmod(file_name, stat.S_IRWXU | stat.S_IRWXG)
	subprocess.check_output(["bash", file_name], shell=False).decode("utf-8")
	os.remove(file_name)

	with open(out_file, "r") as input:
		lines = list(map(lambda each_line: each_line.strip(), input.readlines()))
		return_value = list( filter(lambda each_line: len(each_line)>0, lines) )
	os.remove(out_file)
	return return_value


if __name__=="__main__":
	# find path to session by id: 
	if len(sys.argv)<2:
		print("session name should be specified")
		sys.exit(1)
	hdfs_command = """hdfs dfs -ls /ingestor/%s/ | awk '{print $8}'""" % sys.argv[1]	
	folders = execute_line(hdfs_command)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## stdout to null

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/subprocess/stdout-to-null.py) -->
<!-- The below code snippet is automatically added from ../../python/subprocess/stdout-to-null.py -->
```py
import os
import subprocess

FNULL = open(os.devnull, 'w')
retcode = subprocess.call(['echo', 'foo'], stdout=FNULL, stderr=subprocess.STDOUT)

# It is effectively the same as running this shell command:
# retcode = os.system("echo 'foo' &> /dev/null")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## subprocess example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/subprocess/subprocess-example.py) -->
<!-- The below code snippet is automatically added from ../../python/subprocess/subprocess-example.py -->
```py
import subprocess

print("#call method return status of the message ")
print("command result: ", subprocess.call("ls", shell=False))

print("#check_call method return status of the message ")
print("command result: ", subprocess.check_call("ls", shell=False))

print("#check_output method return status of the message ")
print("command result: ", subprocess.check_output(["ls", ".."]).splitlines())


# for CentOS/RedHat projects need to use
# subprocess.call(["bash","java -jar my_app.jar"], shell=False)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


