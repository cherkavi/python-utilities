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