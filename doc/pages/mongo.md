# mongo

## json2mongo

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/mongo/json2mongo.py) -->
<!-- The below code snippet is automatically added from ../../python/mongo/json2mongo.py -->
```py
import argparse
import logging
import os
import column_mapper
import json
from pymongo import MongoClient


def process_json(path_to_file, mongo_collection):
    with open(path_to_file) as f:
        json_file = json.load(f)
    mongo_collection.insert_one(json_file)


def main(source_folder, processed_folder, error_folder, mongo_collection):
    for each_file in os.listdir(source_folder):
        source_file = os.path.join(source_folder, each_file)
        logging.info("processing file: " + each_file)
        try:
            process_json(source_file, mongo_collection)
            column_mapper.move_file(source_file, processed_folder)
        except RuntimeError as ex:
            logging.error("can't parse/write file: %s  error is: %s " % (source_file, ex.args[0]))
            column_mapper.move_file(source_file, error_folder)


# --sourceFolder /home/technik/projects/temp/zip-tester/source
# --processedFolder /home/technik/projects/temp/zip-tester/processed
# --errorFolder /home/technik/projects/temp/zip-tester/error
# --mongoUrl mongodb://localhost:27017/
# --mongoUser vitalii
# --mongoPassword vitalii
# --mongoDatabase ista-db
# --mongoCollection signals


if __name__ == "__main__":
    app_description = """ 
    read JSON files from Folder and insert them into MongoDB
    sourceFolder - source with JSON
    mongoUrl - url to mongo server, example "mongodb://localhost:27017/"
    mongoUser - user
    mongoPassword - password
    mongoDatabase - mongo db
    mongoCollection - collection     
    errorFolder - can't read JSON and write it into DB
    processedFolder - were successfully writen"""

    parser = argparse.ArgumentParser(description=app_description)

    parser.add_argument('--sourceFolder'
                        , help='source with JSON files'
                        , required=True)
    parser.add_argument('--processedFolder'
                        , help="folders with successfully written files"
                        , required=False)
    parser.add_argument('--errorFolder'
                        , help="error folder, files here when corrupted data or DB is not reachable "
                        , required=True)
    parser.add_argument('--mongoUrl'
                        , help="url to mongo server, example mongodb://localhost:27017/"
                        , required=True)
    parser.add_argument('--mongoUser'
                        , help="mongo user"
                        , required=True)
    parser.add_argument('--mongoPassword'
                        , help="mongo password"
                        , required=True)
    parser.add_argument('--mongoDatabase'
                        , help="mongo database"
                        , required=True)
    parser.add_argument('--mongoCollection'
                        , help="mongo collection"
                        , required=True)
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)

    mongoClient = MongoClient(args.mongoUrl, username=args.mongoUser, password=args.mongoPassword)
    mongoDb = mongoClient[args.mongoDatabase]
    mongoCollection = mongoDb[args.mongoCollection]

    main(args.sourceFolder,
         args.processedFolder,
         args.errorFolder,
         mongoCollection)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


