# sort

## sort file by datetime

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sort/sort-file-by-datetime.py) -->
<!-- The below code snippet is automatically added from ../../python/sort/sort-file-by-datetime.py -->
```py
class ImportFile:
    EXTENSION_SIZE = 4

    # expect to see string like: "Mobile_Tariff_2018_06_13_13_03.csv"
    def __init__(self, file_name):
        self.file_name = file_name
        self.suffix = file_name[-16-ImportFile.EXTENSION_SIZE:]                # '2018_06_13_13_03.xml'
        self.date = datetime.strptime(self.suffix[0:-ImportFile.EXTENSION_SIZE], "%Y_%m_%d_%H_%M")
        self.prefix = file_name[0:len(file_name)-len(self.suffix)]
        pass

    def __str__(self):
        return self.prefix+"   "+self.suffix


    @staticmethod
    def buckets(list_of_files):
        return_value = set()
        for each_file in list_of_files:
            return_value.add(each_file.prefix)
        return return_value

    @staticmethod
    def files_in_bucket(list_of_files, bucket_name):
        return sorted(filter(lambda x: x.prefix == bucket_name, list_of_files), key=lambda f: f.date, reverse=True)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


