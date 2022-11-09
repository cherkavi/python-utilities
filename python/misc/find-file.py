import os

hash = "md5"
suffix = ".py"

hash_options = [hash[-len:]+suffix for len in range(len(hash)+1, 1, -1) ]
print(hash_options)
for file in os.listdir("."):
	for each_option in hash_options:
		if file.endswith(each_option):
			print(file)
