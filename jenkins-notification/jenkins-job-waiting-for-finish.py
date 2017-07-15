# pip install python-jenkins
# http://python-jenkins.readthedocs.io
import jenkins
import time
import sys
import windows_notification

class Wd_jenkins:

    def __init__(self, url, job):
        self.server = jenkins.Jenkins(url)
        self.job_name = job

     
    def job_active(self, job_name):
        try:
            job_info = self.server.get_job_info(job_name)
            color = job_info["color"]
            return color.index("anime")>=0
        except Exception as ex:
            return False

    def is_active(self):
        return self.job_active(self.job_name)


def main(job_name):
    jenkins = Wd_jenkins('http://hostname:8080/jenkins', "Brand Server/"+job_name)

    # wait until finished
    while jenkins.is_active():
        time.sleep(20)

    w=windows_notification.WindowsBalloonTip()
    w.show("Jenkins job, finished", job_name)

if __name__ == '__main__':
    main(sys.argv[1])


# not working - .jobs_count()
# print(dir(server))

# get all views
# print(server.get_views())

# print(server.get_job_info(job_name)["inQueue"])
# print(server.get_job_info(job_name)["queueItem"])
# print(server.get_job_info(job_name)["color"]) # blue, red, red_anime, blue_anime



