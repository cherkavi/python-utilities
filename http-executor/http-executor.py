from flask import Flask
from flask import request
from flask import jsonify

from flask_restplus import Api
from flask_restplus import Resource
from flask_restplus import reqparse

from werkzeug.middleware.proxy_fix import ProxyFix

import subprocess

PORT=13713


import os, sys, subprocess

def open_file(filename):
    if sys.platform == "win32" or sys.platform == "win64": 
        return os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"        
        # not working properly subprocess.call([opener, filename], shell=False, )
        return os.system(opener+" "+filename+"&")

class Open(Resource):
    def get(self):
        """
        open file with default program 
        waiting for request parameter "path" - path to file
        """
        return open_file(request.args.get("path"))

DEFAULT_UI_EDITOR="code"

class Edit(Resource):
    def get(self):
        """
        edit text file with VisualCode editor ('code' alias)
        waiting for request parameter "path" - path to file
        """
        return os.system(DEFAULT_UI_EDITOR + ' %s &' % (request.args.get("path")))


TERMINAL_TEMPLATE = "xterm -fullscreen -fa 'Monospace' -fs 12 -hold -e %s &"

class Terminal(Resource):
    def get(self):
        """
        execute command in terminal 'xterm'
        waiting for request parameter "command" - command for execution in terminal
        """
        parser = reqparse.RequestParser()
        parser.add_argument('command', type=str, help='command line that should be executed')
        args = parser.parse_args()
        return os.system(TERMINAL_TEMPLATE % (args["command"], ) )


if __name__ == "__main__":
    app = Flask("command executor")
    app.wsgi_app = ProxyFix(app.wsgi_app)
    api = Api(
        app=app,
        title="executor of commands",
        default="Available Endpoints",
        default_label="utility",
        description="it is serving for open file and execute bash command in standard terminal",
    )
    api.add_resource(Terminal, "/terminal", endpoint="terminal")
    api.add_resource(Open, "/open", endpoint="open")
    api.add_resource(Edit, "/edit", endpoint="edit")
    app.run(host="0.0.0.0", port=PORT, debug=False)
