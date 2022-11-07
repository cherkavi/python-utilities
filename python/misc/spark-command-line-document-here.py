# orc folder record counter
# subprocess.check_output(["spark2-shell", "--deploy-mode", "client", "<<<", "MARKER_END_DOCUMENT", ":quit", "MARKER_END_DOCUMENT"])
# hdfs dfs -ls /processed/datateam/ingestor_v5/cfb72a80-ec76-43dc-af72-7458c2f40fcb/Can
# val myDataFrame = spark.read.orc("/processed/datateam/ingestor_v5/cfb72a80-ec76-43dc-af72-7458c2f40fcb/Can") 
# val result = myDataFrame.count()

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
	hdfs_command = """hdfs dfs -ls /processed/datateam/ingestor_v5/%s/ | awk '{print $8}'""" % sys.argv[1]	
	folders = execute_line(hdfs_command)

	folders_list = "%s" % folders
	scala_script = """
spark2-shell --deploy-mode client << MARKER_END_DOCUMENT
var counter:Long = 0
val folders = Seq(%s)
for(each_folder<-folders){
	var folder = each_folder.trim()
	if(folder.length()!=0) {
		println(each_folder)
		var frame = spark.read.format("orc").load(each_folder)
		var current_counter = frame.count	
		println(">"+current_counter+"<")
		counter = counter+current_counter
	}
}
println(">>>"+counter+"<<<")
:quit
MARKER_END_DOCUMENT
	""" % folders_list[1:-1].replace("'","\"")
	scala_script_file = "out.scala"
	with open(scala_script_file, "w") as output:
		output.write(scala_script)
	print(scala_script)
	out = subprocess.check_output(["spark2-shell", "--deploy-mode", "client", "<<<", "MARKER_END_DOCUMENT", ":quit", "MARKER_END_DOCUMENT"])
	print(out)
