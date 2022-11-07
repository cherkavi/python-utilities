#!/usr/bin/env python3
from flask import Flask
from flask import request
from flask import jsonify

from flask_restplus import Api
from flask_restplus import Resource
from flask_restplus import reqparse

from werkzeug.middleware.proxy_fix import ProxyFix

import os, sys

def open_file(filename):
    if sys.platform == "win32" or sys.platform == "win64": 
        return os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"        
        # not working properly subprocess.call([opener, filename], shell=False, )
        return os.system(opener+" "+filename+"&")


class Open(Resource):
    ARGUMENT_NAME = "path"
    def get(self):
        """
        open file with default program 
        
        :param path: request parameter - path to file
        :return: system code of execution
        :rtype: int
        """
        # request.args.get("path"))
        args = reqparse \
            .RequestParser() \
            .add_argument(Open.ARGUMENT_NAME,
                          type=str,
                          help='path to file that should be opened with default app',
                          required=True,
                          nullable=False) \
            .parse_args()
        return open_file(args[Open.ARGUMENT_NAME])


class Edit(Resource):
    DEFAULT_UI_EDITOR = "code"
    ARGUMENT_NAME = "path"
    def get(self):
        """
        edit text file with VisualCode editor ('code' alias)

        :param path: request parameter - path to file
        :return: system code of execution
        :rtype: int
        """
        # request.args.get("path"))
        args = reqparse \
            .RequestParser() \
            .add_argument(Edit.ARGUMENT_NAME,
                          type=str,
                          help='path to file that should be edited',
                          required=True,
                          nullable=False) \
            .parse_args()
        return os.system(Edit.DEFAULT_UI_EDITOR + ' %s &' % (args[Edit.ARGUMENT_NAME]))


class Terminal(Resource):
    TERMINAL_TEMPLATE = "xterm -fullscreen -fa 'Monospace' -fs 12 -hold -e %s &"
    ARGUMENT_NAME = "command"
    def get(self):
        """
        execute command in terminal 'xterm'

        :param command: request parameter - command for execution in terminal
        :return: system code of execution
        :rtype: int
        """
        args = reqparse\
            .RequestParser()\
            .add_argument(Terminal.ARGUMENT_NAME,
                          type=str,
                          help='command line that should be executed',
                          required=True,
                          nullable=False)\
            .parse_args()
        return os.system(Terminal.TERMINAL_TEMPLATE % (args[Terminal.ARGUMENT_NAME], ))


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
    app.run(host="0.0.0.0", port=13413, debug=False)

    # examples:
    # http://localhost:13413/edit?path=%22/home/technik/hello.txt%22
    # http://localhost:13413/edit?path=%22$HOME/hello.txt%22
    #
    # http://localhost:13413/terminal?command=%22docker%20ps%20-a%22
    #
    # http://localhost:13413/open?path=%22/home/technik/hello.txt%22