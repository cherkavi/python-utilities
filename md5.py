#!/usr/bin/python

# python 2.7.x 
# import md5 as md5hash from md5
# print(md5("hello"))

# python 3.5.x
import hashlib
hashlib.md5(open('/home/technik/projects/temp/ista/json-source/2018110815330826780340100-2018110815330829280340100-956.json','rb').read().encode("utf-8")).hexdigest()

hashlib.md5(b"hello").hexdigest()
brand="temp"
sku="my_code"
hashlib.md5(f"{brand}{sku}".encode("utf-8")).hexdigest()
