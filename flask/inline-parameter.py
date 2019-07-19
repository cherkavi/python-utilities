from flask import Flask
from flask import request
from flask import jsonify

import subprocess

# example of triggering app
# http://localhost:3000/?message=PATH

app = Flask(__name__)
# api = Api(app=app)

@app.route("/<job_id>", methods=['GET'])
def get_simulation_job(job_id):
    return jsonify(message="job id is: {}!".format(job_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
