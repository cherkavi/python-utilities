[sqlalchemy examples](https://www.programcreek.com/python/example/51986/sqlalchemy.sql.text)

postgresql connection string
```
# pip3 install psycopg2-binary
postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"
```

database connection
```python
db.engine.execute(text("SELECT 1"))
```

Logging example
```
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

flask_app.config['SQLALCHEMY_ECHO'] = settings.SQLALCHEMY_ECHO
```

Error:
```text
sqlAlchemy detached instance error
```
https://docs.sqlalchemy.org/en/13/orm/session_api.html
```python
        with db.engine.connect() as connection:
            session = Session(bind=connection, expire_on_commit=expire_on_commit)
            return_value = logic(session)
            if commit:
                session.commit()
            return return_value
```

table update
```python


def update_with_new_default(connection: Connection):
    statement_clear = t_zur_image.update() \
        .values(is_default=0) \
        .where(t_zur_image.user_id == user_id, t_zur_image.listing_id == listing_id)
    statement_set = t_zur_image.update() \
        .values(is_default=1) \
        .where(t_zur_image.user_id == user_id, t_zur_image.listing_id == listing_id,
                t_zur_image.image_id == image_id_default)
    connection.execute(statement_clear)
    connection.execute(statement_set)
    return True


return_value = connection_aware(update_with_new_default)


t_zur_image = Table(
    'zur_image', metadata,
    Column('image_id', Integer, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('listing_id', Integer, nullable=False),
    Column('image_name', String, nullable=False),
    Column('is_default', Integer, nullable=False)
)

```

save record
```python

def session_aware(logic: Callable[[Session], Any], commit=False, expire_on_commit=True):
    """
    wrapper for executing ORM "queries"
    :param logic: - function with one parameter - session
    :param commit: commit after function execution
    :param expire_on_commit: when you need to have DetachedORM Object for View
    :return:
    """
    session = None
    try:
        with db.engine.connect() as connection:
            session = Session(bind=connection, expire_on_commit=expire_on_commit)
            return_value = logic(session)
            if commit:
                session.commit()
            return return_value
    finally:
        if session:
            session.close()


def connection_aware(logic: Callable[[Connection], Any]):
    """
    wrapper for executing native queries
    :param logic: - function with one parameter - connection
    :return: result of function
    """
    with db.engine.connect() as connection:
        return logic(connection)


session_aware(lambda session: session.add(HlmImage.build(user_id, listing_id, image_name)), commit=True)

```

select object
```python
return session.query(Message) \
        .filter(Message.process_flag == id, Message.showed > 0)
	.order_by(Message.id.desc())
```

update object
```python
        image: HlmImage = session_aware(lambda session: session.query(HlmImage)
                                        .filter(HlmImage.image_id==image_without_name.image_id)
                                        .update({"image_name":image_name}), commit=True)
```

long lasting records processing ( records loop )
```python
# error text: can't update object from different Thread 
engine = create_engine(f"sqlite:///{db_path}?cache=shared", echo=False, connect_args={'check_same_thread': False})
```
