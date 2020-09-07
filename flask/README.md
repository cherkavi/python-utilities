http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/  
[nice example](https://github.com/postrational/rest_api_demo)

throw exception
```python
                # raise werkzeug.exceptions.NotFound('LawFirms not exists by id')
                lawfirm_namespace.abort(404, 'LawFirm not exists by provided id')
```

flask view, flask complex return view
```python
    'pgroups': fields.List(cls_or_instance=fields.String(required=True, description='id of groups'),
                           attribute=lambda x: x["pgroups"].split(",")),
    'practices': fields.List(cls_or_instance=fields.String(required=True, description='practices'),
                             attribute=lambda x: x["practices"].split(","))
```

header, header request
```python
    @namespace.response(200, "by user ")
    # !!! DON'T USER UNDERSCORE !!!
    @namespace.param(name="userid", description="id of user", _in="header")
    def get(self):
        input_arg = reqparse.RequestParser()\
            .add_argument(name="userid", type=int, location="headers")\
            .parse_args()
        user_id = input_arg["userid"]

```

> No API definition provided.
need to check all 'object_view'
```python
@namespace.marshal_with(object_view)
```

initialization
```python

    @app.before_first_request
    def load_db_settings(engine=None):
        if engine is None:
            engine = db.engine
        with engine.connect() as connection:
            settings.load_database_config(connection)

```

DateTime, datetime, default datetime, onupdate
```python
    # added = Column(DateTime, nullable=False, server_default=sqlalchemy.sql.func.now())
    # added = Column(DateTime, nullable=False, server_default=text('NOW()'))

    first_created = Column(DateTime(), default=datetime.datetime.now)
    last_modified = Column(DateTime(), onupdate=datetime.datetime.now)
```
