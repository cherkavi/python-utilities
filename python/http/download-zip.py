#!/usr/bin/env python
import requests
import shutil
import time

def main():
	host="localhost"
	port=8808
	brand_name="mywcard2go"
	file_name=brand_name+".zip"
	url = "http://%s:%i/published/resources/%s" % (host, port, file_name)
	for i in range(1,3):
		current_time = time.time()
		response = requests.get(url, stream=True)
		local_file_name = file_name+str(i)
		with open(local_file_name, "wb") as output_file:
			response.raw.decode_content = True
			shutil.copyfileobj(response.raw, output_file)
		print( local_file_name + " " + response.headers["Content-MD5"] )
		print( time.time()-current_time)
if __name__=='__main__':
	main()
	
# f0b70d245eae21e9c46bd4b94cad41cc *affin-1482164837000.zip
# 91372ab88e402460f2a832ef2c44a834 *affin-1484662020000.zip

#1482164837000
#1484662020000