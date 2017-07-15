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