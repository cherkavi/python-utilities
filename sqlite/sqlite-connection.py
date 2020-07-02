import os
import sqlite3
from datetime import datetime

path_to_database = os.environ.get("PATH_TO_SQLITE")
if not path_to_database:
    path_to_database = "file::memory:?cache=shared"

if __name__ == '__main__':
    connection = sqlite3.connect(path_to_database)
    connection.execute("""CREATE TABLE if not exists messages (
	receive_time timestamp,
	message_group text,
	message_url text,
	message_title text,
	message_full_url text,
    black_marker_reason text);""")

    connection.execute("insert into messages (message_group, message_title, receive_time) values (?, ?, ?)",
                       (u"Java-Entwicklung group", u"message #1", datetime.now()))
    connection.execute("insert into messages (message_group, message_title, receive_time) values (?, ?, ?)",
                       (u"Python-Entwicklung group", u"message #2",
                        # datetime parsing, parsing datetime, datetimeformat
                        datetime.strptime("01/07/2020,  3:46 PM", '%d/%m/%Y, %I:%M %p')))
    connection.commit()
    single_value = connection.execute("select * from messages where message_group = ?",
                                      ("Java-Entwicklung group",)).fetchone()
    print(single_value)

    for each_record in connection.execute("select * from messages where message_group is not null"):
        print(each_record)

    connection.close()
