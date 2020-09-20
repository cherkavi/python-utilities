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

Download file
```python
@image_namespace.route('/item/<int:image_id>/<int:size_id>')
@image_namespace.response(404, 'Image(s) by Listing id not found.')
class Image(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self._log = logging.getLogger(self.__class__.__name__)

    @image_namespace.doc("get one image by id")
    @image_namespace.response(200, "file from external storage")
    @image_namespace.response(404, "can't find image")
    @image_namespace.response(500, "can't download image from external storage ")
    @image_namespace.produces(['image/png', 'image/bmp', 'image/jpeg', 'image/gif', 'image/tiff', 'image/webp'])
    def get(self, image_id: int, size_id: int):
        """
        Returns image by image_id ( ask /items endpoint )
        and number of size_id ( 75, 250, 500, 1000 )
        """
        image: OrmImage = session_aware(lambda session:
                                        session.query(OrmImage).filter_by(image_id=image_id).one_or_none())
        if not image:
            return {"message": "image not found"}, 404

        client_download_file_path = StorageUtils.get_path_to_download_file(image.image_name, size_id)
        server_uploaded_file_path = StorageUtils.get_path_to_upload_file(image.image_name, size_id)
        if not StorageClass().is_exist(server_uploaded_file_path):
            return {"message": "can't find image in external storage "}, 404
        if not StorageClass().load(server_uploaded_file_path, client_download_file_path):
            return {"message": "can't download image from external storage "}, 500
        image_file_path = unarchive_file(client_download_file_path)
        image_format = image_utils.get_file_format(image_file_path)
        return send_file(image_file_path,
                         mimetype=f"image/{image_format}",
                         as_attachment=True,
                         attachment_filename=image.image_name)

```