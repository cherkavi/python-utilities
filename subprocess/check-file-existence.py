import subprocess
try:
	value = subprocess.check_call(["ls","/data/store/collected/car-data/4f1a-a1b4-4bee05c9c281/MDF4/20181129T105009.MF4"], shell=False, stderr=None, stdout=None)
except Exception as e:
	print(e.returncode)
else:
	print("OK")
