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