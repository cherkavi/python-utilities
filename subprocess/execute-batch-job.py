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
