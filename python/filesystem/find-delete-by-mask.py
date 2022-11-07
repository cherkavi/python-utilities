  def delete(self, object_path_in_storage: str) -> bool:
        try:
            for each_file in glob.glob(f"/tmp/temp_folder/file_nam*"):
                os.remove(each_file)
            return True
        except:
            return False
