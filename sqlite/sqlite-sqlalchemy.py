import os
import sqlite3

from sqlalchemy.engine import create_engine, Transaction

path_to_database = os.environ.get("PATH_TO_SQLITE")
if path_to_database:
    path_to_database = f"sqlite://{path_to_database}?cache=shared"
else:
    path_to_database = f"sqlite:///:memory:?cache=shared"

if __name__ == '__main__':

    engine = create_engine(path_to_database, echo=True)
    connection = engine.connect()

    connection.execute("""CREATE TABLE if not exists messages (
	receive_time timestamp,
	message_group text,
	message_url text,
	message_title text,
	message_full_url text,
    black_marker_reason text);""")

    transaction:Transaction = connection.begin()
    connection.execute("insert into messages (message_group, message_title) values (?, ?)",
                       (u"Java-Entwicklung group", u"message #1"))
    transaction.commit()
    single_value = connection.execute("select * from messages where message_group = ?",
                                      ("Java-Entwicklung group",)).fetchone()
    print(single_value)

    connection.close()
