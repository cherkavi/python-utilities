#!/usr/bin/env python
import paramiko, time, cherkavi

def get_tomcat_processes():
	try:
		ssh = paramiko.SSHClient()
		# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.load_system_host_keys()
		ssh.connect("hostname", username=cherkavi.linux_login, password=cherkavi.linux_password)
		# dir(ssh)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ps -fC java")
		lines = ssh_stdout.readlines()
		return lines[1:]
	finally:
		ssh.close()
	

def get_tomcat_process_count():
	'''
	calculate amount of processes which were executed by "tomcat" user
	'''
	return len(get_tomcat_processes())

while get_tomcat_process_count() < 2:
	print time.ctime()
	time.sleep(30)
print "second process was found "+time.ctime()
print get_tomcat_processes()