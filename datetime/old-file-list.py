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
