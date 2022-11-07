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

