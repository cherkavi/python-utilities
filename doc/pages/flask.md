# flask

## app with doc

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/flask/app-with-doc/flask-app.py) -->
<!-- The below code snippet is automatically added from ../../python/flask/app-with-doc/flask-app.py -->
```py
from flask import Flask, request
from flask import jsonify

from flask_restplus import Api, reqparse
from flask_restplus import Resource
from werkzeug.middleware.proxy_fix import ProxyFix


class Health(Resource):

    # curl -X GET -F 'result={"status":"OK"}' 127.0.0.1:5000/readiness-check
    # @google_maps_namespace.marshal_with(google_maps_search_candidate, as_list=True)
    # @google_maps_namespace.doc(params={"command": "text for searching on Google Maps"})
    def get(self):
        # request.args.get("path")
        # or
        # parser = reqparse.RequestParser()
        # parser.add_argument('command', type=str, help='command line that should be executed')
        # args = parser.parse_args()
        print(request.values['result'])
        return jsonify(message="readiness probe")

    # curl -X POST -F 'result={"status":"OK"}' 127.0.0.1:5000/readiness-check
    def post(self):
        print(request.data)
        return jsonify(message="readiness probe")


if __name__ == "__main__":
    app = Flask("my app")
    app.wsgi_app = ProxyFix(app.wsgi_app)
    api = Api(
        app=app,
        title="example app",
        default="Available Endpoints",
        default_label="label1, "
        "label2, "
        "label3",
        description="Powered by technik",
    )
    api.add_resource(Health, "/readiness-check")
    app.run(host="0.0.0.0")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## app

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/flask/app.py) -->
<!-- The below code snippet is automatically added from ../../python/flask/app.py -->
```py
from flask import Flask, jsonify
import logging
import os

DEFAULT_APP_NAME = "test-app"
DEFAULT_PORT = 4000


class FlaskApp:
    def __init__(self, application_name: str, port: int = DEFAULT_PORT):
        self._name: str = application_name
        self._app: Flask = Flask(self._name)
        self._port: int = port
        self._logger: logging.Logger = None
        self._app.add_url_rule("/echo/<input_message>", view_func=self.echo)
        self._logger = self._app.logger
        self._logger.setLevel(logging.DEBUG)

    def run(self):
        self._app.run(port=self._port)

    @property
    def app(self):
        return self._app

    def echo(self, input_message) -> str:
        self._logger.info("test request")
        return jsonify(message=f"message is: {input_message}!")


if __name__ == "__main__":
    FlaskApp(DEFAULT_APP_NAME).run()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## app_error

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/flask/app_error.py) -->
<!-- The below code snippet is automatically added from ../../python/flask/app_error.py -->
```py
import logging

import werkzeug
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import HTTPException

import settings

api = Api(version='1.0',
          title='db-react-bridge',
          description='facade with business logic for directories')

log = logging.getLogger(__name__)


# @api.errorhandler(Exception)
# def default_error_handler(e):
#     # log.exception(message)
#     return {'message': 'unexpected exception'}, 500

# @api.errorhandler(NoResultFound)
# def database_not_found_error_handler(e):
#     # log.warning(traceback.format_exc())
#     return {'message': 'no data found'}, 404


for each_code in (list(range(400, 420)) + list(range(501, 520))):
    # class Exception400(HTTPException):
    #     code = 400
    #     # description = ()
    class_exception_by_code: type = type(f'Exception{each_code}',
                                         (HTTPException,),
                                         {"__doc__": f"exception for code {each_code}",
                                          "code": each_code})

    # werkzeug.http.HTTP_STATUS_CODES[402]='xxxx'
    werkzeug.exceptions._aborter.mapping[each_code] = class_exception_by_code
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## echo

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/flask/echo.py) -->
<!-- The below code snippet is automatically added from ../../python/flask/echo.py -->
```py
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('/path/to/file.cfg')

@app.route("/")
def hello():
    return "hello world!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## flask cors manual

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/flask/flask-cors-manual.py) -->
<!-- The below code snippet is automatically added from ../../python/flask/flask-cors-manual.py -->
```py
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
            # response.headers.add('Access-Control-Allow-Origin', request.headers['origin'])
            # response.headers.add('Access-Control-Allow-Origin', '*')
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## flask restful cors authorize

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/flask/flask-restful-cors-authorize.py) -->
<!-- The below code snippet is automatically added from ../../python/flask/flask-restful-cors-authorize.py -->
```py
import config

from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
api = Api(app)
if app.config['CORS_ENABLED'] is True:
    CORS(app, origins="http://127.0.0.1:8080", allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        supports_credentials=True)


@app.before_request
def authorize_token():
    if request.endpoint != 'token':
        try:
            authorize_jwt(request)
        except Exception as e:
            return "401 Unauthorized\n{}\n\n".format(e), 401


class GetToken(Resource):
    def post(self):
        token = generate_jwt()
        return token       # token sent to client to return in subsequent requests in Authorization header


# requires authentication through before_request decorator
class Test(Resource):
    def get(self):
        return {"test": "testing"}


api.add_resource(GetToken, '/token', endpoint='token')
api.add_resource(Test, '/test', endpoint='test')

if __name__ == '__main__':
    app.run()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## inline parameter

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/flask/inline-parameter.py) -->
<!-- The below code snippet is automatically added from ../../python/flask/inline-parameter.py -->
```py
from flask import Flask
from flask import request
from flask import jsonify
import os
import uuid
import jsonschema
import subprocess

# example of triggering app
# http://localhost:3000/?message=PATH

app = Flask(__name__)
# api = Api(app=app)


@app.route("/<job_id>", methods=['GET'])
def get_simulation_job(job_id):
    return jsonify(message="job id is: {}!".format(job_id))


@app.route("/simulation", methods=['POST'])
def create_simulation_job():
    # post request read data
    job_request = request.get_json(silent=True)
    job_id = uuid.uuid1()
    return job_id


@app.route("/scenario-extraction/<uuid:job_id>", methods=['GET'])
def get_scenario_extraction_job(job_id):
    # return code 
    return jsonify(message="some message %s" % (str(job_id))), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## test_app

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/flask/test_app.py) -->
<!-- The below code snippet is automatically added from ../../python/flask/test_app.py -->
```py
from flask_testing import TestCase

from flask import Flask, jsonify
from app import FlaskApp

class MyTest(TestCase):

    def create_app(self) -> Flask:
        self.flask_app = FlaskApp("test")
        self.flask_app.app.testing = True
        return self.flask_app.app

    def test_server_up_and_running(self):
        # given
        control_string: str = "test1"
        with self.flask_app.app.test_client() as test_client:

        # when
            response = test_client.get(f"/echo/{control_string}")

        # then
        assert response.status_code == 200
        assert response.json["message"] is not None
        assert response.json["message"].find(control_string) > 0
        print(response)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## var printer

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/flask/var-printer.py) -->
<!-- The below code snippet is automatically added from ../../python/flask/var-printer.py -->
```py
from flask import Flask
from flask import request

import subprocess

# example of triggering app
# http://localhost:3000/?message=PATH

app = Flask(__name__)

@app.route("/")
def execute_application():
    # job_request = request.get_json(silent=True)
    remote_request_argument = request.args.get("message")
    # result = subprocess.check_output(["tail /home/projects/current-task/results.output"], shell=True).decode("utf-8").splitlines()
    result = subprocess.check_output(["echo $"+remote_request_argument], shell=True).splitlines()
    return "<br />".join(result)
    return ("result of your request is <b>%s</b> " % result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


