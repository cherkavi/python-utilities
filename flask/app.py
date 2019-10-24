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
