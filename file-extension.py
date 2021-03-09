import os

path = '/home/projects/sampledoc.docx'
root, extension = os.path.splitext(path)

print('Root:', root)
print('extension:', extension)
