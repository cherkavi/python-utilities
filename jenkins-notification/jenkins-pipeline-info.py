# pip install python-jenkins
# http://python-jenkins.readthedocs.io
import jenkins


class Wd_jenkins:
    JOB_SWORDFISH = "%s-int-run-swordfish-all-tests"
    ALL_JOBS = [
        "%s-dev-compile",
        "%s-dev-build-catfish",
        "%s-dev-rpms",
        "%s-int-undeploy-apps",
        "%s-int-deploy-testenv",
        "%s-int-prepare-db",
        "%s-dev-setupdb",
        "%s-dev-sql_script",
        "%s-int-deploy-brands",
        "%s-int-deploy-web-server",
        "%s-int-prepare-testenv",
        "%s-dev",
        "%s-dev-component",
        "%s-int-build-functional-test",
        "%s-int-run-catfish-all-tests",
        "%s-int-redeploy-testenv"
    ]

    def __init__(self, url, pipeline_prefix):
        self.server = jenkins.Jenkins(url)
        self.job_swordfish = Wd_jenkins.JOB_SWORDFISH % (pipeline_prefix)
        self.job_list = []
        for each_job in Wd_jenkins.ALL_JOBS:
            self.job_list.append(each_job % (pipeline_prefix))
        self.job_list.append(self.job_swordfish)

     
    def job_active(self, job_name):
        try:
            job_info = self.server.get_job_info(job_name)
            color = job_info["color"]
            return color.index("anime")>=0
        except Exception as ex:
            return False


    def swordfish_active(self):
        return self.job_active(self.job_swordfish)

    def pipeline_active(self):
        for each_job in self.job_list:
            if self.job_active(each_job):
                return True
        return False


int09 = Wd_jenkins('http://hostname:8080/jenkins', "QA")
print("Pipeline is active: " + str(int09.pipeline_active()))
print("Swordfish is active: " + str(int09.swordfish_active()))

# not working - .jobs_count()
# print(dir(server))

# get all views
# print(server.get_views())

# print(server.get_job_info(job_name)["inQueue"])
# print(server.get_job_info(job_name)["queueItem"])
# print(server.get_job_info(job_name)["color"]) # blue, red, red_anime, blue_anime



