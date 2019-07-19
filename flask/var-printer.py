from flask import Flask
from flask import request

import subprocess

# example of triggering app
# http://localhost:3000/?message=PATH

app = Flask(__name__)

@app.route("/")
def execute_application():
    remote_request_argument = request.args.get("message")
    result = subprocess.check_output(["echo $"+remote_request_argument], shell=True).splitlines()
    return ("result of your request is <b>%s</b> " % result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
