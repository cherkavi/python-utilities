# filesystem

## archiver

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/archiver/batch_archiver.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/archiver/batch_archiver.py -->
```py
import shutil
import os
from datetime import datetime

class ImportFile:
    EXTENSION_SIZE = 4

    # expect to see string like: "Mobile_Tariff_2018_06_13_13_03.csv"
    def __init__(self, file_name):
        self.file_name = file_name
        self.suffix = file_name[-16-ImportFile.EXTENSION_SIZE:]                # '2018_06_13_13_03.xml'
        self.date = datetime.strptime(self.suffix[0:-ImportFile.EXTENSION_SIZE], "%Y_%m_%d_%H_%M")
        self.prefix = file_name[0:len(file_name)-len(self.suffix)]
        pass

    def __str__(self):
        return self.prefix+"   "+self.suffix


    @staticmethod
    def buckets(list_of_files):
        return_value = set()
        for each_file in list_of_files:
            return_value.add(each_file.prefix)
        return return_value

    @staticmethod
    def files_by_bucket(list_of_files, bucket_name):
        return sorted(filter(lambda x: x.prefix == bucket_name, list_of_files), key=lambda f: f.date, reverse=True)


class Logger:

    def __init__(self, path_to_file):
        self.out = open(path_to_file, "a")

    def write(self, message):
        self.out.write(message)
        self.out.write("\n")
        self.out.flush()

    def __del__(self):
        self.out.close()


def standard_archiving(files_in_bucket, source_folder, destination_folder):
    if len(files_in_bucket) < 2:
        return

    for each_file in files_in_bucket[1:]:
        path_to_file = os.path.join(source_folder, each_file.file_name)
        logger.write("move file: "+path_to_file)
        shutil.move(path_to_file, destination_folder)


def archive(source_folder, destination_folder, archive_function):
    import_files = [ImportFile(each_file) for each_file in os.listdir(source_folder)]
    for each_bucket_name in ImportFile.buckets(import_files):
        archive_function(ImportFile.files_by_bucket(import_files, each_bucket_name), source_folder, destination_folder)


if __name__ == '__main__':
    archive_folder = "archive"
    root_folder = "/home/technik/temp/import/"
    logger = Logger("/home/technik/temp/archive.txt")
    try:
        for each_folder in ["Mobile"]:
            archive(root_folder+each_folder, archive_folder, standard_archiving)
    finally:
        del logger
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## brand xml clear

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/brand-xml-clear.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/brand-xml-clear.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## calculate files

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/calculate-files.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/calculate-files.py -->
```py
'''
calculate amount of files inside folder
'''
import sys
import os
import time
import datetime

def main(argv):
    while True:
        dt = datetime.datetime.fromtimestamp(time.time())
        print ( dt.strftime('%Y-%m-%dT%H:%M:%S'), "   ",  len(os.listdir(argv[0])) )
        time.sleep(1)

if __name__ == "__main__":
   main(sys.argv[1:])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## copy list of file to dest

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/copy-list-of-file-to-dest.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/copy-list-of-file-to-dest.py -->
```py
import sys
import os
import shutil


def main(path_to_list, destination_folder):
    """ copy list of file into destination folder
    :param path_to_list: text file with list of files
    :param destination_folder: full path to destination folder
    """
    with open(path_to_list) as input_file:
        for each_line in input_file:
            file_candidate = each_line.strip()
            # is file exists, existance of file
            if os.path.isfile(file_candidate):
                print("%s %s" % (destination_folder,file_candidate))
                shutil.copy(file_candidate, destination_folder)


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("input parameters should be: <text file with list of files to be copied> <destination folder>")
        exit(1)
    main(sys.argv[1], sys.argv[2])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## cp

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/cp.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/cp.py -->
```py
import shutil;shutil.copyfile('/tmp/1.txt', '/tmp/2.txt')
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## create remove folder

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/create-remove-folder.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/create-remove-folder.py -->
```py
import os
# pip install pytest-shutil
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## find delete by mask

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/find-delete-by-mask.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/find-delete-by-mask.py -->
```py
  def delete(self, object_path_in_storage: str) -> bool:
        try:
            for each_file in glob.glob(f"/tmp/temp_folder/file_nam*"):
                os.remove(each_file)
            return True
        except:
            return False
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## memory file

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/memory-file.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/memory-file.py -->
```py
import StringIO

memfile = StringIO.StringIO()

try:

	memfile.write("hello string")

	memfile.seek(0)

	print(memfile.read())

finally:
	memfile.close()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## old file list

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/old-file-list.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/old-file-list.py -->
```py
from datetime import timedelta
from datetime import datetime
import time
import os

if __name__=='__main__':
	folder = "c:\\temp\\"
	delta = timedelta(days=30)

	for each_file in os.listdir(folder):
		path_to_file = os.path.join(folder,each_file)
		file_timestamp = datetime.fromtimestamp(os.stat(path_to_file).st_ctime)
		if file_timestamp+delta<datetime.now():
			# os.remove(path_to_file)
			print(path_to_file)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## print_current_path

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/print_current_path.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/print_current_path.py -->
```py
import os
print( os.path.abspath(os.path.dirname(__file__)) )
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## remover

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/remover/remove_old_files.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/remover/remove_old_files.py -->
```py
import os
import sys
import re
import datetime

# application to remove files with filtering by name ( regular expression ) and by creation date ( how old )

def action_for_older_than_days(folder, action, matchers):
	for each_file in os.listdir(folder):
		matchers_result = [each_matcher(folder, each_file) for each_matcher in matchers]
		if all(matchers_result):
			action(control_folder, each_file)


def remove_file(folder, filename):
	os.unlink(os.path.join(folder, filename))


def match_file_by_mask(folder, filename):
	return re.search("refdata_all(.*).sql", filename) is not None


def match_file_by_date(folder, filename):
	# return datetime.datetime.fromtimestamp(os.stat(os.path.join(folder, filename)).st_ctime) < datetime.datetime.now()-datetime.timedelta(days=180)
	return datetime.datetime.fromtimestamp(os.stat(os.path.join(folder, filename)).st_ctime) < datetime.datetime.now()-datetime.timedelta(seconds=100)

# expected to have command line parameter with name of the folder, otherwise hard-coded value will be applied
if __name__=="__main__":
	control_folder = "/data/wmu/"

	if len(sys.argv)>1:
		control_folder = sys.argv[1]

	# print("working folder: " + control_folder)

	if not os.path.exists(control_folder):
		print("path is not exists")
		sys.exit(1)

	if not os.path.isdir(control_folder):
		print("path is file, expected folder")
		sys.exit(2)

	action_for_older_than_days(control_folder, remove_file, [match_file_by_mask, match_file_by_date])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## temp file

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/filesystem/temp-file.py) -->
<!-- The below code snippet is automatically added from ../../python/filesystem/temp-file.py -->
```py
# temp file
# temp-file
import tempfile
print(tempfile.mktemp())
```
<!-- MARKDOWN-AUTO-DOCS:END -->


