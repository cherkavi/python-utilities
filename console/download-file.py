#!/usr/bin/env python

# download file via http and save it locally

import requests
from tqdm import tqdm

def main():
	url = "http://localhost:8808/published/resources/affin.zip.md5"
	for i in range(1,10):
		response = requests.get(url, stream=True)
		file_name = "affin.zip.md5"+str(i)
		with open(file_name, "wb") as handle:
	    		for data in tqdm(response.iter_content()):
        			handle.write(data)
		print( file_name + " " + response.headers["Content-MD5"])

if __name__=='__main__':
	main()
	
# f0b70d245eae21e9c46bd4b94cad41cc *affin-1482164837000.zip
# 91372ab88e402460f2a832ef2c44a834 *affin-1484662020000.zip

#1482164837000
#1484662020000