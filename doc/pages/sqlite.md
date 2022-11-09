# sqlite

## sqlite connection

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sqlite/sqlite-connection.py) -->
<!-- The below code snippet is automatically added from ../../python/sqlite/sqlite-connection.py -->
```py
import os
import sqlite3
from datetime import datetime

# f"sqlite://{db_path}:?cache=shared"
# sqlite:///:memory: (or, sqlite://)
# sqlite:///relative/path/to/file.db
# sqlite:////absolute/path/to/file.db
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## sqlite sqlalchemy orm

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sqlite/sqlite-sqlalchemy-orm.py) -->
<!-- The below code snippet is automatically added from ../../python/sqlite/sqlite-sqlalchemy-orm.py -->
```py
from __future__ import annotations

import os
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path_to_database = os.environ.get("PATH_TO_SQLITE")
if path_to_database:
    path_to_database = f"sqlite://{path_to_database}?cache=shared"
else:
    path_to_database = f"sqlite:///:memory:?cache=shared"

Base = declarative_base()


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(types.Integer, primary_key=True)
    receive_time = Column('receive_time', types.DateTime)
    message_group = Column('message_group', types.String(255))
    message_url = Column('message_url', types.String(128))
    message_title = Column('message_title', types.String(255))
    message_full_url = Column('message_full_url', types.String(255))
    black_marker_reason = Column('black_marker_reason', types.String(64))
    content = Column('content', types.Text(), default=u'')

    def __str__(self):
        return f"id:{self.id}  receive_time: {self.receive_time} message_title: {self.message_title} " \
               f"message_url: {self.message_url}  message_full_url: {self.message_full_url}"


if __name__ == '__main__':
    engine = create_engine(path_to_database, echo=True)
    Base.metadata.create_all(engine, checkfirst=True)
    session_builder: sessionmaker = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    session = session_builder()
    # session.begin()
    message = Messages()
    message.message_title = "hello"
    message.receive_time = datetime.now()
    session.add(message)
    session.commit()
    message = Messages()
    message.message_title = "hello2"
    message.receive_time = datetime.now()
    session.add(message)
    session.commit()

    session_another = session_builder()
    object_message: Messages = session_another.query(Messages).filter_by(message_title="hello").one_or_none()
    object_message.message_full_url = "https://this.is.some_url.com"
    session_another.add(object_message) # not possible to attach to another session session.add(object_message)
    session_another.commit()

    # read multiply objects, read updates from another transaction
    # alchemy operations "http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters"
    for each_record in session.query(Messages).filter(Messages.message_title.isnot(None)):
        print(each_record)
    # connection = engine.connect()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## sqlite sqlalchemy

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/sqlite/sqlite-sqlalchemy.py) -->
<!-- The below code snippet is automatically added from ../../python/sqlite/sqlite-sqlalchemy.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->


