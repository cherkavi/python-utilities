import urllib2

try:
	url_response = urllib2.urlopen('http://ecsd0010072c.epam.com:9999/__admin/')
	if url_response.getcode() != 200:
		print(" return code is "+str(url_response.getcode()))
	else:
		print("ok");
	// print(dir(url_response))
except Exception as e:
	print("no connection "+e.message)
# print(url_response)
