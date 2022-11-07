from flask import Flask
from flask import request
from flask import jsonify
import os
import uuid
import jsonschema
import subprocess

# example of triggering app
# http://localhost:3000/?message=PATH

app = Flask(__name__)
# api = Api(app=app)


@app.route("/<job_id>", methods=['GET'])
def get_simulation_job(job_id):
    return jsonify(message="job id is: {}!".format(job_id))


@app.route("/simulation", methods=['POST'])
def create_simulation_job():
    # post request read data
    job_request = request.get_json(silent=True)
    job_id = uuid.uuid1()
    return job_id


@app.route("/scenario-extraction/<uuid:job_id>", methods=['GET'])
def get_scenario_extraction_job(job_id):
    # return code 
    return jsonify(message="some message %s" % (str(job_id))), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
