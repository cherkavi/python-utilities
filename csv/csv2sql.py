import csv
from typing import List
import mariadb


sql_request_insert_files = "INSERT INTO hlm_aws_images (image_id, image_name, image_format) VALUES (?, ?, ?)"

def insert_record(record_connection, id: int, name: str, format: str):
    record_connection.execute(sql_request_insert_files, (str(id), name, format))

def retrieve_id(value:str) -> int:
    elements:List[str] = value.split("-")
    return int(elements[len(elements)-1])

connection = mariadb.connect( 
        host="127.0.0.1",
        port=3310,
        user="xing",
        passwd="xing",
        database="xing"
    )
connection.autocommit=True
cursor = connection.cursor()

with open("/home/technik/Dropbox/projects/law-marketing/current_task/image-prod-issue/prod-images.csv") as csv_file:
    reader = csv.reader(csv_file,delimiter=',')
    is_header = False # no header
    for row in reader:
        if is_header:
            is_header = False
            continue
        insert_record(cursor, retrieve_id(row[2]), row[2], row[3])        

connection.close()