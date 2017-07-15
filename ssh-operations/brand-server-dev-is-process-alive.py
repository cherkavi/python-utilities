#!/usr/bin/env python
import sys, paramiko, time, cherkavi

def get_process_by_id(id):
	try:
		ssh = paramiko.SSHClient()
		# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.load_system_host_keys()
		ssh.connect("hostname", username=cherkavi.linux_login, password=cherkavi.linux_password)
		# dir(ssh)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ps -p "+str(id))
		lines = ssh_stdout.readlines()
		return lines[1:]
	finally:
		ssh.close()

if __name__=="__main__":
	proc_id=sys.argv[1]
	while len(get_process_by_id(proc_id)) > 0:
		print time.ctime()
		time.sleep(15)
	print "process %s was not found %s " % (proc_id, time.ctime())