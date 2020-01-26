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
