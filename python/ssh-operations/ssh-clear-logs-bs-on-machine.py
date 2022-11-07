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