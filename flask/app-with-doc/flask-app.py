from flask import Flask
from flask import jsonify

from flask_restplus import Api
from flask_restplus import Resource
from werkzeug.middleware.proxy_fix import ProxyFix



class Health(Resource):
    def get(self):
        # request.args.get("path")
        # or
        # parser = reqparse.RequestParser()
        # parser.add_argument('command', type=str, help='command line that should be executed')
        # args = parser.parse_args()
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
