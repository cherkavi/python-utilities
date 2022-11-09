# mysqldb

## mariadb batch

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/mysqldb/mariadb-batch.py) -->
<!-- The below code snippet is automatically added from ../../python/mysqldb/mariadb-batch.py -->
```py
import sys
import mysql.connector


def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3310,
        user="root",
        passwd="example",
        database="files"
    )


sql_request_select_session = "select id from sessions where name=%s"
sql_request_insert_files = "INSERT INTO files (id_vendor, id_session, name, size) VALUES (%s, %s, %s, %s)"


def find_sessionId_if_exists(cursor, session_name):
    cursor.execute(sql_request_select_session, (session_name, ))
    try:
        return cursor.fetchone()[0]
    except Exception as e:
        return None


def insert_batch(db, cursor, list_of_elements):
    # cursor.execute(id_vendor, id_session, name, size)
    cursor.executemany(sql_request_insert_files, list_of_elements)
    db.commit()

BATCH_LIMIT = 100

if __name__=='__main__':
    db = get_db()
    cursor = db.cursor()
    counter = 0
    batch = list()
    for each_line in sys.stdin:        
        clear_line = each_line.strip()
        if len(clear_line)==0:
            # empty line 
            continue
        values = clear_line.split(" ")
        vendor_id = 2        
        session_id = find_sessionId_if_exists(cursor, values[1])
        if not session_id:
            continue
        # logger/subfolder/filename
        name = values[2]+"/"+values[3]+"/"+values[4]
        size = values[0]
        batch.append( (vendor_id, session_id, name, size) )
        if len(batch)>=BATCH_LIMIT:
            insert_batch(db, cursor, batch)
            del batch[:]
            counter = counter + cursor.rowcount

    if len(batch)>0:
        insert_batch(db, cursor, batch)        
        counter = counter + cursor.rowcount
    print(counter)
    cursor.close()
#  cat intel-filelist.txt | awk -F ' ' '{print $5$8}' | awk -F '/' '{print $1" "$10" "$11" "$12" "$13}' | python sql-insert-files-size-intel.py
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## mariadb connect

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/mysqldb/mariadb-connect.py) -->
<!-- The below code snippet is automatically added from ../../python/mysqldb/mariadb-connect.py -->
```py
# docker container: https://github.com/cherkavi/docker-images/blob/master/mariadb/docker-compose.yml
# sudo apt-get python-mysqldb
# python -m pip install mysql-connector
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  port=3310,
  user="root",
  passwd="example",
  database="files"
)


# sudo apt-get install libmariadbclient-dev
# pip3 install mariadb

# Module Imports
import mariadb
import sys 

# Connect to MariaDB Platform
try: conn = mariadb.connect( 
    user="db_user", 
    password="db_user_passwd", 
    host="192.0.2.1", 
    port=3306, 
    database="employees" 
) except mariadb.Error as e: 
    print(f"Error connecting to MariaDB Platform: {e}") 
    sys.exit(1) 


cursor = mydb.cursor()

cursor.execute("select * from vendor")
for each_record in cursor:
  print(each_record)

cursor.execute("show tables")
for each_record in cursor:
  print(each_record)


# request = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# parameters = ("John", "Highway 21")
# cursor.execute(request, parameters)
# mydb.commit()
# print(mycursor.rowcount, "record inserted.")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## select big query

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/mysqldb/select-big-query.py) -->
<!-- The below code snippet is automatically added from ../../python/mysqldb/select-big-query.py -->
```py
import mysql.connector


def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3310,
        user="root",
        passwd="example",
        database="files"
    )


sql_request_select_files = "select concat(vendor.path, sessions.path,'/',sessions.name, '/', files.name) from files inner join vendor on files.id_vendor=vendor.id and vendor.id=2  inner join sessions on sessions.id=files.id_session"

if __name__=='__main__':
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql_request_select_files)
    for each_record in cursor:
    	print(each_record[0])
    cursor.close()
    db.close()
```
<!-- MARKDOWN-AUTO-DOCS:END -->


