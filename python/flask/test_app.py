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
