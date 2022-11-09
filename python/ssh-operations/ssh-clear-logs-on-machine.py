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