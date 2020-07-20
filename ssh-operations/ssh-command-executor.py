#!/usr/bin/env python
# ssh remote command execution and return value
# ssh return value
# ssh command execution
from typing import List
import sys, paramiko

user_name = "data-user"
user_pass = "data-pass"
host_name = "ubsdpdesp00013.vantage.org"

def execute_command(command:str) -> List[str]:
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.load_system_host_keys()
		ssh.connect(host_name, username=user_name, password=user_pass)
		# dir(ssh)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
		return [each_line.strip("\n") for each_line in ssh_stdout.readlines()]
	finally:
		ssh.close()

if __name__=="__main__":
    print(execute_command("pwd"))
