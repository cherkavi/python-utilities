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
