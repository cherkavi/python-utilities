# pip3 install psycopg2-binary
import os
import psycopg2

DB_VARIANT_HOST=os.environ.get("DB_VARIANT_HOST")
DB_VARIANT_DATABASE=os.environ.get("DB_VARIANT_DATABASE")
DB_VARIANT_USERNAME=os.environ.get("DB_VARIANT_USERNAME")
DB_VARIANT_PASSWORD=os.environ.get("DB_VARIANT_PASSWORD")
DB_VARIANT_PORT=os.environ.get("DB_VARIANT_PORT")
DB_VARIANT_PREFIX=os.environ.get("DB_VARIANT_PREFIX")


connection = psycopg2.connect(host=DB_VARIANT_HOST, port=DB_VARIANT_PORT, database=DB_VARIANT_DATABASE, user=DB_VARIANT_USERNAME, password=DB_VARIANT_PASSWORD)
connection.autocommit = False

cursor = connection.cursor()
cursor.execute(f"DELETE FROM {DB_VARIANT_PREFIX}_variant;")
cursor.execute(f"DELETE FROM {DB_VARIANT_PREFIX}_variant_key;")
connection.commit()

# cursor.execute(f"select * FROM {DB_VARIANT_PREFIX}_variant;")
# cursor.execute(f"select * FROM {DB_VARIANT_PREFIX}_variant_key;")
# print([each_record[1] for each_record in cursor.fetchall()])

connection.close()
        

