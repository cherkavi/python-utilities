import zipfile
import os

files = ["1.txt","2.txt","3.txt"]
with zipfile.ZipFile('out.zip', 'w') as zipper:        
    for file in files:
        zipper.write(file, compress_type=zipfile.ZIP_DEFLATED)
        # os.remove(file)