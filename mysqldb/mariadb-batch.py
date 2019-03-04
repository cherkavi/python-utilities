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
        if len(batch)<BATCH_LIMIT:
            batch.append( (vendor_id, session_id, name, size) )
        else:
            insert_batch(db, cursor, batch)
            del batch[:]
        counter = counter + cursor.rowcount

    if len(batch)>0:
        insert_batch(db, cursor, batch)        
    print(counter)
    cursor.close()
#  cat intel-filelist.txt | awk -F ' ' '{print $5$8}' | awk -F '/' '{print $1" "$10" "$11" "$12" "$13}' | python sql-insert-files-size-intel.py
