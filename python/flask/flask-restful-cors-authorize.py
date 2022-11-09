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
