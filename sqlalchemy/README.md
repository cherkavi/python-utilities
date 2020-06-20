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

