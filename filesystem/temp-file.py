# temp file
# temp-file
import tempfile
import os
file_path=tempfile.mktemp()
print(file_path)
# print name of the file, get filename
os.path.basename(file_path)
