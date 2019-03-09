import os
import shutil
import sys


output_folder = "test_folder/test1"

# folder check existence
if os.path.exists(output_folder):
	# checking is directory, isdirectory ?
	# if not os.path.isdir(control_folder):

	# remove folder, delete folder
	# shutil.os.remove(output_folder)
	shutil.rmtree(output_folder)

# create folder 
os.makedirs(output_folder)


