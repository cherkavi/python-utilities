import os
import shutil
import sys


output_folder = "test_folder/test1"

if os.path.exists(output_folder):
	shutil.os.remove(output_folder)

os.makedirs(output_folder)


