# parameter-for-app

## parameter reader

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/parameter-for-app/parameter-reader.py) -->
<!-- The below code snippet is automatically added from ../../python/parameter-for-app/parameter-reader.py -->
```py
import os

settings_filename = "path-to-file.settings___"
environment_variable = "EXPORT_IMPORT_FOLDER"

def read_path_to_file():
    # attempt to read data from file
    if os.path.exists(settings_filename):
        with open(settings_filename) as f:
            return f.readlines()[0]

    # attempt to read data from ENV variable
    if environment_variable in os.environ:
        return os.environ[environment_variable]

    # return current folder, when script exists
    return os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    # os.path.join(folder, filename)
    print(read_path_to_file())
```
<!-- MARKDOWN-AUTO-DOCS:END -->


