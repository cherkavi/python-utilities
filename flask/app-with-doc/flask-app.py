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
