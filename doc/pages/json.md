# json

## json example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/json/json-example.py) -->
<!-- The below code snippet is automatically added from ../../python/json/json-example.py -->
```py
import json

example = {"a":10, "b":20}
# convert to json string
print(json.dumps(example))
# convert to json string and then move back to object 
#              - read from string
print(json.loads(json.dumps(example, sort_keys=True, indent=4)))


class Example:
    def __init__(self, value):
    	self.value = value

    def __str__(self):
    	return self.value

# is not JSON serializable - using pickle
#print(json.dumps(Example("hello")))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## json2csv

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/json/json2csv.py) -->
<!-- The below code snippet is automatically added from ../../python/json/json2csv.py -->
```py
import json
import logging
import os
import sys
import column_mapper


def main(path_to_json, path_to_csv):
    with open(path_to_json) as f:
        json_file = json.load(f)
    need_column = True
    with open(path_to_csv, "w") as output:
        for each_row in json_file["Data"]:
            if need_column:
                need_column = False
                output.write(",".join([column_mapper.column_by_value(key) for key, value in each_row.items()]))
                output.write("\n")
            output.write(",".join([str(value) for key, value in each_row.items()]))
            output.write("\n")


if __name__ == "__main__":
    app_description = """ 
    read JSON file and convert it into CSV
    """
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)

    file_json = sys.argv[1]
    if not os.path.exists(file_json):
        logging.error("file does not exists: " + file_json)
    file_csv = sys.argv[2]

    main(file_json, file_csv)

    # pretty print
    print(json.dumps("{'one': 'two', 'three': 'four'}", indent=4, sort_keys=True))
```
<!-- MARKDOWN-AUTO-DOCS:END -->


