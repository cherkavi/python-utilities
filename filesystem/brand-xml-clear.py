import os
import shutil

root_dir = "C:\\temp\\brands\\"
for each_dir in os.listdir(root_dir):
	subfolder = root_dir + each_dir
	for subfolder_root, subfolder_dirs, subfolder_files in os.walk(subfolder):
		for each_dir in subfolder_dirs:
			candidate = subfolder + "\\" +each_dir
			if os.path.isdir(candidate):
				shutil.rmtree(candidate)
		for each_file in subfolder_files:
			if each_file != 'brand.xml':
				full_file_name = subfolder_root + "\\" + each_file
				os.unlink(full_file_name)
			

print ( "done" )
	
