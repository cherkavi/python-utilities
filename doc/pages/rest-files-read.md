# rest-files-read

## readfilesrest

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/rest-files-read/readfilesrest/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/rest-files-read/readfilesrest/__init__.py -->
```py

```
<!-- MARKDOWN-AUTO-DOCS:END -->



## readfilesrest

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/rest-files-read/readfilesrest/main.py) -->
<!-- The below code snippet is automatically added from ../../python/rest-files-read/readfilesrest/main.py -->
```py
import configparser
import sys
import os
import json
import tornado.ioloop
import tornado.web

endpoint_list = r"/list/([a-zA-Z\-0-9\.:,/_]*)"
endpoint_file = r"/file/([a-zA-Z\-0-9\.:,/_]+)"


class ListFolder:

    def __init__(self, path_to_folder):
        file_list = self.read_from_folder(path_to_folder)
        self.files = [subfolder_files for subfolder_files in file_list]
        self.index = -1

    @staticmethod
    def read_from_folder(path):
        try:
            return os.listdir(path)
        except:
            raise tornado.web.HTTPError(404, "folder not found: " + path)

    def __iter__(self):
        return self

    def __next__(self):
        self.index = self.index + 1
        if self.index >= len(self.files):
            raise StopIteration()
        else:
            return self.files[self.index]


class ListHandler(tornado.web.RequestHandler):

    def initialize(self, folder):
        self.folder = folder

    def get(self, relative_path):
        # endpoint contains regexp and everything will be inside 'relative_path'
        self.write(json.dumps([each for each in ListFolder(self.folder + relative_path)]))


class FileHandler(tornado.web.RequestHandler):

    def initialize(self, folder):
        self.folder = folder

    def get(self, relative_path):
        buffer_size = 512000
        # endpoint contains regexp and everything will be inside 'relative_path'
        file_path = self.folder + relative_path
        if not os.path.exists(file_path):
            raise tornado.web.HTTPError(404, "file not exists: " + relative_path)
        if not os.path.isfile(file_path):
            raise tornado.web.HTTPError(400, "it is not a file: " + relative_path)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + os.path.basename(file_path))
        with open(file_path, 'r') as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                self.write(data)
        self.finish()


def main(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file)

    folder = config["local"]["folder"]
    listen_port = config["remote"]["port"]

    app = tornado.web.Application([
        (endpoint_file, FileHandler, dict(folder=folder)),
        (endpoint_list, ListHandler, dict(folder=folder)),
    ])
    app.listen(listen_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main(sys.argv[1])


# read file 
#        with open(f"${path_to_messages}/${each_message.content_file}","r") as each_message_file_content:
#            message_content = each_message_file_content.readlines()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## setup

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/rest-files-read/setup.py) -->
<!-- The below code snippet is automatically added from ../../python/rest-files-read/setup.py -->
```py
from distutils.core import setup
setup(
    name="read-files-rest",
    packages=["readfilesrest"],
    version="1.0.0",
    description="read files from folder and provide access to them via HTTP ",
    author="Vitalii Cherkashyn",
    author_email="technik7job@gmail.com",
    keywords=["REST", "Download files"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: prototype",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Components :: REST app",
        ],
    long_description="""\
    provide ability for external users ( http interface ) 
    to read files from local filesystem  
"""
)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


