import base64

print(base64.encodestring('login:password'.encode()))
print(base64.encodestring('weblogic:weblogic1'.encode()))


#               with open(path_to_image_file, "rb") as f:
#                   encoded = base64.b64encode(f.read())

