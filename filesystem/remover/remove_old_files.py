import os
import sys
import re
import datetime

def action_for_older_than_days(folder, action, matchers):
	for each_file in os.listdir(folder):
		matchers_result = [each_matcher(folder, each_file) for each_matcher in matchers]
		if all(matchers_result):
			action(control_folder, each_file)


def remove_file(folder, filename):
	print(os.path.join(folder, filename))


def match_file_by_mask(folder, filename):
	return re.search("refdata_all(.*).sql", filename) is not None


def match_file_by_date(folder, filename):
	# return datetime.datetime.fromtimestamp(os.stat(os.path.join(folder, filename)).st_ctime) < datetime.datetime.now()-datetime.timedelta(days=180)
	return datetime.datetime.fromtimestamp(os.stat(os.path.join(folder, filename)).st_ctime) < datetime.datetime.now()-datetime.timedelta(seconds=100)


if __name__=="__main__":
	control_folder = "c:\\temp\\remover\\test\\"

	if not os.path.exists(control_folder):
		print("path is not exists")
		sys.exit(1)

	if not os.path.isdir(control_folder):
		print("path is file, expected folder")
		sys.exit(2)

	action_for_older_than_days(control_folder, remove_file, [match_file_by_mask, match_file_by_date])

