import sys
import subprocess
import os
import stat

def execute_line(command_line):
	file_name = "1.sh"
	with open(file_name, "w") as output:
		output.write(command_line)
	os.chmod(file_name, stat.S_IRWXU | stat.S_IRWXG)
	return_value = subprocess.check_output(["bash", file_name], shell=False).decode("utf-8")
	os.remove(file_name)

execute_line("ls -la > out.txt")
