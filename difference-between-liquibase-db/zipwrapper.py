import zipfile
import os
import tempfile
import shutil


class ZipWrapper:

    def __init__(self, path_to_file):
        self.zip_reference = zipfile.ZipFile(path_to_file, 'r')
        self.file_list = [each_entry.filename for each_entry in self.zip_reference.infolist()]

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, "zip_reference"):
            self.zip_reference.close()

    @staticmethod
    def __check_candidate__(filename, entry_name):
        if filename.find(entry_name) >= 0:
            return filename
        else:
            return None

    def get_entry(self, entry_name):
        for each_entry in self.file_list:
            candidate = self.__check_candidate__(each_entry, entry_name)
            if candidate is not None:
                return candidate
        return None

    def get_entries(self, entry_name):
        return_value = list()
        for each_entry in self.file_list:
            candidate = self.__check_candidate__(each_entry, entry_name)
            if candidate is not None:
                return_value.append(candidate)
        return return_value

    def copy_entry_to_file(self, entry_name, destination_file):
        """ :return full path to created file """
        try:
            temp_folder = tempfile.mkdtemp()
            path_to_created_file = self.zip_reference.extract(entry_name, temp_folder)
            try:
                os.remove(destination_file)
            except FileNotFoundError:
                pass
            os.rename(path_to_created_file, destination_file)
            return destination_file
        finally:
            if 'temp_folder' in locals():
                shutil.rmtree(temp_folder, True)

    def extract(self, folder):
        self.zip_reference.extractall(folder)

    def copy_entries_to_folder(self, entries, destination_folder):
        """ :return full path to created folder !!! NOT WORKING !!! """
        try:
            temp_folder = tempfile.mkdtemp()
            for each_entry in entries:
                try:
                    path_to_created_file = self.zip_reference.extract(each_entry, temp_folder)
                except KeyError:
                    continue
                path = [each for each in each_entry.split("/") if each != '']
                print(path)
                destination_file = os.path.join(destination_folder, *path)
                try:
                    os.remove(destination_file)
                except FileNotFoundError:
                    pass
                if os.path.isdir(path_to_created_file):
                    continue
                os.rename(path_to_created_file, destination_file)
            return destination_folder
        finally:
            if 'temp_folder' in locals():
                shutil.rmtree(temp_folder, True)
