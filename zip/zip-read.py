import zipfile
import os

with zipfile.ZipFile('out.zip', 'r') as zipper:        
    for file in zipper.namelist():
        zipper.extract(file, file+".restored")
		# each_file = zipper.read(file)
        # os.write(file+".restored", each_file)
        # print(file, each_file)
        # os.remove(file)