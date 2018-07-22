#!/usr/bin/env python3
import subprocess
import re
import time
import sys


def run_command_find_answer(command, prefix, suffix):
    '''
    run console command, read result of console command,
    parse console output and find string between markers
    return None when marker was not found
    '''
    process_output = subprocess.check_output(command, shell=False).decode("utf-8")
    result = re.search(prefix+"(.*)"+suffix, process_output)
    if len(result.groups())>0:
        return result.group(1)
    else:
        return None

if __name__ == '__main__':
    command = "./return_result_emulator.sh"
    attempts = 100
    sleep_time = 30

    for _ in range(attempts):
        # print(script_response.groups())
        result = run_command_find_answer(command, ">>>","<<<")
        if not result:
            # print("marker was not found")
            sys.exit(1)                
        if result == "RUNNING":
            # print("still running ...")
            time.sleep(sleep_time)
            continue
        if result == "SUCCESS":
            # print("success")
            sys.exit(0)
        if result == "FAIL":
            # print("fail")
            sys.exit(2)
        # unknown return string 
        sys.exit(1) 
    # timeout
    sys.exit(1)
    