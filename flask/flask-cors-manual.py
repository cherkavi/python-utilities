def configure_app(app):
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_URL - do not set it up, bug of Flask + Docker
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_POOL_SIZE'] = settings.SQLALCHEMY_POOL_SIZE
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_ECHO'] = settings.SQLALCHEMY_ECHO
    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    app.config['ENV'] = settings.FLASK_ENV
    app.config['PREFERRED_URL_SCHEME'] = settings.FLASK_URL_SCHEME
    app.config['MAX_CONTENT_LENGTH'] = settings.FLASK_MAX_CONTENT_LENGTH

    @app.after_request
    def add_cors_headers(response: Response) -> Response:
        # remote_client = request.referrer[0:request.referrer.find("/", 9)] if request.referrer else request.remote_addr
        # nginx settings:
        # proxy_set_header X-Real-IP $remote_addr
        remote_client = request.remote_addr
        if remote_client in settings.SERVERS_WHITE_LIST:
            response.headers.add('Access-Control-Allow-Origin', remote_client)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
            response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
            response.headers.add('Access-Control-Allow-Headers', 'Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        else:
            log.debug(f"CORS params: referrer: {request.referrer}   remote_addr:{request.remote_addr}")
            log.info(f"CORS policy: {remote_client} not in {settings.SERVERS_WHITE_LIST}")
        return response


def create_app() -> Flask:
    app = Flask(__name__)
    configure_app(app)

    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    db.init_app(app)

    @app.before_first_request
    def load_db_settings(engine=None):
        if engine is None:
            engine = db.engine
        with engine.connect() as connection:
            settings.load_database_config(connection)

    return app

