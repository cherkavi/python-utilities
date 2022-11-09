# zip

## zip archive unarchive

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/zip/zip-archive-unarchive.py) -->
<!-- The below code snippet is automatically added from ../../python/zip/zip-archive-unarchive.py -->
```py
import logging
import os
import subprocess
from typing import List

log = logging.getLogger(__name__)


def archive_files(paths: List[str]) -> List[str]:
    """
    archive list of files
    :param paths: list of paths that should be archived
    :return: list of archived files
    """
    return [archive_file(each_file) for each_file in paths]


def archive_file(path: str) -> str:
    """
    :param path: full path to file
    :returns path_to_archive_file
    """
    try:
        compressed_file = f"{path}.zip"
        if subprocess.check_call(["zip", "-1", "--junk-paths", compressed_file, path], shell=False) == 0:
            return compressed_file
        else:
            return None
    except subprocess.CalledProcessError as e:
        log.warning(f"can't zip file {path}")
        return None


def unarchive_file(path: str) -> str:
    """
    :param path: full path to file
    :returns path_to_archive_file
    """
    try:
        if subprocess.check_call(["unzip", "-o", path, "-d", os.path.dirname(path)], shell=False) == 0:
            return path[:-4]
        else:
            return None
    except subprocess.CalledProcessError as e:
        log.warning(f"can't zip file {path}")
        return None
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## zip read

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/zip/zip-read.py) -->
<!-- The below code snippet is automatically added from ../../python/zip/zip-read.py -->
```py
import zipfile
import os

with zipfile.ZipFile('out.zip', 'r') as zipper:        
    for file in zipper.namelist():
        zipper.extract(file, file+".restored")
		# each_file = zipper.read(file)
        # os.write(file+".restored", each_file)
        # print(file, each_file)
        # os.remove(file)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## zip write

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/zip/zip-write.py) -->
<!-- The below code snippet is automatically added from ../../python/zip/zip-write.py -->
```py
import zipfile
import os

files = ["1.txt","2.txt","3.txt"]
with zipfile.ZipFile('out.zip', 'w') as zipper:        
    for file in files:
        zipper.write(file, compress_type=zipfile.ZIP_DEFLATED)
        # os.remove(file)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


