import sys
import subprocess
import os
import stat

def execute_line(command_line):
	file_name = "1.sh"
	out_file = "out.txt"
	with open(file_name, "w") as output:
		output.write(command_line+" > "+out_file)
	os.chmod(file_name, stat.S_IRWXU | stat.S_IRWXG)
	subprocess.check_output(["bash", file_name], shell=False).decode("utf-8")
	os.remove(file_name)

	with open(out_file, "r") as input:
		lines = list(map(lambda each_line: each_line.strip(), input.readlines()))
		return_value = list( filter(lambda each_line: len(each_line)>0, lines) )
	os.remove(out_file)
	return return_value


if __name__=="__main__":
	# find path to session by id: 
	if len(sys.argv)<2:
		print("session name should be specified")
		sys.exit(1)
	hdfs_command = """hdfs dfs -ls /ingestor/%s/ | awk '{print $8}'""" % sys.argv[1]	
	folders = execute_line(hdfs_command)

