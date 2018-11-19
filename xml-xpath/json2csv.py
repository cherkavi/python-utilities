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
