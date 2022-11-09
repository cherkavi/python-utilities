# ssh-operations

## brand server dev is process alive

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ssh-operations/brand-server-dev-is-process-alive.py) -->
<!-- The below code snippet is automatically added from ../../python/ssh-operations/brand-server-dev-is-process-alive.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## brand server dev tomcat process count

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ssh-operations/brand-server-dev-tomcat-process-count.py) -->
<!-- The below code snippet is automatically added from ../../python/ssh-operations/brand-server-dev-tomcat-process-count.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## ssh brandserver version checker

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ssh-operations/ssh-brandserver-version-checker.py) -->
<!-- The below code snippet is automatically added from ../../python/ssh-operations/ssh-brandserver-version-checker.py -->
```py
#!/usr/bin/env python
import paramiko
import cherkavi

def main():
	host = 'hostname'
	user = cherkavi.linux_login
	secret = cherkavi.linux_password
	port = 22

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=port)
	stdin, stdout, stderr = client.exec_command('sudo yum list | grep brandserver')
	package_name = stdout.read().decode("utf-8").strip()
	print(package_name[package_name.find("noarch")+8: package_name.rfind(".noarch")])
	client.close()	

if __name__ == "__main__":
	main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## ssh clear logs bs on machine

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ssh-operations/ssh-clear-logs-bs-on-machine.py) -->
<!-- The below code snippet is automatically added from ../../python/ssh-operations/ssh-clear-logs-bs-on-machine.py -->
```py
#!/usr/bin/env python
import paramiko
import cherkavi
import sys

def execute_commands(client):
	client.exec_command("sudo rm -f /var/log/brand-server/*.gz")
	client.exec_command("sudo rm -f /var/log/brand-server/*-1.log*")
	client.exec_command("sudo rm -f /var/log/brand-server/*.txt")
	client.exec_command("sudo rm -f /var/log/brand-server/*.log-*")
	client.exec_command("sudo rm -f /var/log/brand-server/catalina.log-2017*")
	client.exec_command("sudo rm -f /var/log/brand-server/catalina.out-2017*")
	client.exec_command("sudo rm -f /var/log/brand-server/catalina.out")
	client.exec_command("sudo rm -f /var/log/brand-server/brand-server.log")
	client.exec_command("sudo /etc/init.d/tomcat_brand-server restart")

def main(host):
	user = cherkavi.linux_login
	secret = cherkavi.linux_password
	port = 22
	print("clean host %s " % (host,) )
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=port)
	execute_commands(client)
	client.close()	

if __name__ == "__main__":
	if len(sys.argv) <=1 :
		host = 'hostname'
	else:
		host = sys.argv[1]
	main(host)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## ssh clear logs on machine

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ssh-operations/ssh-clear-logs-on-machine.py) -->
<!-- The below code snippet is automatically added from ../../python/ssh-operations/ssh-clear-logs-on-machine.py -->
```py
#!/usr/bin/env python
import paramiko
import cherkavi
import sys

def execute_commands(client):
	client.exec_command("sudo rm -f /var/log/*.gz")
	client.exec_command("sudo rm -rf /var/log/cron-2017*")
	client.exec_command("sudo rm -rf /var/log/messages-2017*")
	client.exec_command("sudo rm -rf /var/log/secure-2017*")
	client.exec_command("sudo rm -rf /var/log/up2date-2017*")

	client.exec_command("sudo rm -f /var/log/brand-server/*.gz")
	client.exec_command("sudo rm -f /var/log/brand-server/*-1.log*")
	client.exec_command("sudo rm -f /var/log/brand-server/*.txt")
	client.exec_command("sudo rm -f /var/log/brand-server/*.log-*")
	client.exec_command("sudo rm -f /var/log/brand-server/catalina.log-2017*")
	client.exec_command("sudo rm -f /var/log/brand-server/catalina.out-2017*")
	client.exec_command("sudo rm -f /var/log/brand-server/catalina.out")
	client.exec_command("sudo rm -f /var/log/brand-server/brand-server.log")
	client.exec_command("sudo /etc/init.d/tomcat_brand-server restart")

	client.exec_command("sudo rm -f /var/log/weblogic10/*.out00*")
	client.exec_command("sudo rm -f /var/log/weblogic10/*.log00*")
	client.exec_command("sudo rm -f /var/log/weblogic10/*.gz")
	client.exec_command("sudo rm -f /var/log/weblogic10/*.2017*.log")
	client.exec_command("sudo rm -f /var/log/weblogic10/*.log-*")
	client.exec_command("sudo rm -f /var/log/weblogic10/app/*tar.gz")
	client.exec_command("sudo rm -f /var/log/weblogic10/app/*-1.gz")
	client.exec_command("sudo rm -f /var/log/weblogic10/patch_2017*.log")

def main(host):
	user = cherkavi.linux_login
	secret = cherkavi.linux_password
	port = 22
	print("clean host %s " % (host,) )
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=port)
	execute_commands(client)
	client.close()	

if __name__ == "__main__":
	if len(sys.argv) <=1 :
		host = 'hostname'
	else:
		host = sys.argv[1]
	main(host)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## ssh command executor

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ssh-operations/ssh-command-executor.py) -->
<!-- The below code snippet is automatically added from ../../python/ssh-operations/ssh-command-executor.py -->
```py
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
#        url = f"{airflow_url}/api/experimental/dags/{airflow_dag_name}/dag_runs"
#        airflow_pass_fixed='"'+airflow_pass+'"'
#        command = f"curl --data-binary {data_body} -u {airflow_user}:{airflow_pass_fixed} -X POST {url}"
#        print(airflow_user, airflow_pass_fixed, data_body)
#        return self.execute_command(command, True)
	
    print(execute_command("pwd"))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## ssh command repeater

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/ssh-operations/ssh-command-repeater.py) -->
<!-- The below code snippet is automatically added from ../../python/ssh-operations/ssh-command-repeater.py -->
```py
#!/usr/bin/env python
import paramiko
import cherkavi

def main():
	host = 'hostname'
	user = cherkavi.linux_login
	secret = cherkavi.linux_password
	port = 22

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=port)
	stdin, stdout, stderr = client.exec_command("ls -la /var/log/horus-swordfish/ | grep log | awk '{print $5}'")
	result = stdout.read().decode("utf-8").strip()
	print(result)
	client.close()	

if __name__ == "__main__":
	while True:
		main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->


