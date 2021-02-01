http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/  
[nice example](https://github.com/postrational/rest_api_demo)

throw exception
```python
                # raise werkzeug.exceptions.NotFound('LawFirms not exists by id')
                lawfirm_namespace.abort(404, 'LawFirm not exists by provided id')
```

flask namespace
```python
# !!! don't use braces in description !!!
yelp_namespace = Namespace('yelp', description='Yelp review, communication with Yelp API')
```

flask view, flask complex return view
```python
    'pgroups': fields.List(cls_or_instance=fields.String(required=True, description='id of groups'),
                           attribute=lambda x: x["pgroups"].split(",")),
    'practices': fields.List(cls_or_instance=fields.String(required=True, description='practices'),
                             attribute=lambda x: x["practices"].split(","))

    def parse_json_string(record: Dict) -> str:
        try:
            return json.loads(record.answer_options)
        except:
            return record.answer_options

    'answer_options': fields.Raw(description='answer_options', attribute=parse_json_string),

    'practices': fields.Nested(name="practice", as_list=True,
                               model={'practice': fields.Integer(attribute=lambda x: x)},
                               attribute=lambda row: [row['practice1'], row['practice2'], row['practice3']],
                               description="practices, delimited by comma"),			     
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
# for inpath parameter name avoid char '/'
# @image_namespace.route('/item/<int:image_id>/<string:name>')
#
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

Upload file
https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
```python
image_upload_parser = reqparse.RequestParser() \
    .add_argument('image_body', type=FileStorage, location='files', required=True, help='image file')
""" request parser for image """


@image_namespace.route('/items/<int:id>')
class ImageItems(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self._log = logging.getLogger(self.__class__.__name__)

    @image_namespace.response(201, 'image was uploaded and processed')
    @image_namespace.response(400, "request error")
    @image_namespace.response(500, "can't save data in storage ( internal or external ) ")
    @image_namespace.doc(params={'image_body': "image itself", 'listing_id': "id of listing"})
    @image_namespace.marshal_with(image_item_view)
    @image_namespace.expect(image_upload_parser)
    def post(self, listing_id: int):
        """
        add new image to listing
        """

        full_path_to_image, extension = self._save_client_image_to_tempstorage(dir_name, image_name)



    def _save_client_image_to_tempstorage(self, directory_title: str, image_name: str) -> List[str]:
        """
        :param directory_title: directory name
        :param image_name: image name
        :return: [full path to image in temp storage,  file format (jpg, png, gif ....) ]
        """
        try:
            arguments = image_upload_parser.parse_args()
        except Exception as e:
            self._log.warning(f"unexpected user request {e}")
            image_namespace.abort(400, "unexpected user request")
        if not arguments["image_body"]:
            image_namespace.abort(400, "no image found in request ")
        full_path_to_image = StorageUtils.get_path_to_temp_upload(directory_title, image_name)

        file_format = ImageItems._file_extension_from_content_type(arguments['image_body'].content_type.lower())
        full_path_to_image = f"{full_path_to_image}.{file_format}"
        try:
            arguments["image_body"].save(full_path_to_image)
            self._log.info(f"uploaded file saved: {full_path_to_image}")
        except FileNotFoundError as e:
            self._log.error(f"can't save data into temp folder {full_path_to_image}")
            image_namespace.abort(500, "internal storage (temp) error")
        return full_path_to_image, file_format
```


```sh
    app.config['MAX_CONTENT_LENGTH'] = settings.FLASK_MAX_CONTENT_LENGTH

    @app.before_request
    def check_directory(request: Request):
        if (client_origin := get_client_url(request)):


    @app.after_request
    def add_cors_headers(response: Response) -> Response:
        # nginx settings:
        # proxy_set_header X-Real-IP $remote_addr
        remote_client = request.referrer[0:request.referrer.find("/", 9)] if request.referrer else request.remote_addr


    @app.before_first_request
    def load_db_settings(engine=None):
        if engine is None:


    @app.route('/')
    def get():
    	@after_this_request
	def add_header(response):
		return response
```

example of reading all htto request parameters
```python
    @app.before_request
    def check_directory():
        if (client_origin := get_client_url(request)):
            if settings.DEFAULT_ID:
                g.directory_id = settings.DEFAULT_DIRECTORY_ID
            else:
                print("   ".join([f"{each_key}:{request.environ.get(each_key)}" for each_key in request.environ.keys()]))
                print(
                    f">>> {request.url_root}  {request.remote_addr}  {request.referrer}  {request.host_url}  {request.host}  {request.base_url}")
                g.directory_id = settings.LIST.get(client_origin, None)
                if not g.directory_id:
                    log.warning(f"current id is unknown for {client_origin}")

```

```python
def null_int(field_name: str) -> Callable[[RowProxy], Optional[int]]:
    '''
    wrapper for 'fields.Integer' - avoid null value
    ```attribute=null_int('lead_id'))```
    :param field_name: name of Integer field
    :return: function for assigning to 'attribute'
    '''
    def avoid_null(row: RowProxy) -> Optional[int]:
        integer_value = row[field_name]
        if isinstance(integer_value, int):
            return integer_value
        if integer_value and isinstance(integer_value, str) and len(integer_value) and integer_value.isdigit():
            return int(integer_value)
        else:
            return None

    return avoid_null


def position_decoder(field_name: str) -> Callable[[RowProxy], Optional[str]]:
    '''
    wrapper for 'fields.Integer' - avoid null value
    ```attribute=null_int('lead_id'))```
    :param field_name: name of Integer field
    :return: function for assigning to 'attribute'
    '''
    def decode_decimal(row: RowProxy) -> Optional[str]:
        if field_name not in row or row[field_name] is None:
            return ""
        return "%.8f" % row[field_name]
    return decode_decimal
    
```

