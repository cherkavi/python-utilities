# jenkins-notification

## jenkins job waiting for finish

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/jenkins-notification/jenkins-job-waiting-for-finish.py) -->
<!-- The below code snippet is automatically added from ../../python/jenkins-notification/jenkins-job-waiting-for-finish.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## jenkins pipeline info

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/jenkins-notification/jenkins-pipeline-info.py) -->
<!-- The below code snippet is automatically added from ../../python/jenkins-notification/jenkins-pipeline-info.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## windows_notification

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/jenkins-notification/windows_notification.py) -->
<!-- The below code snippet is automatically added from ../../python/jenkins-notification/windows_notification.py -->
```py
from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time

class WindowsBalloonTip:

    def show(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        # self.show_balloon(title, msg)        
    def close(self):
        DestroyWindow(self.hwnd)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

def balloon_tip(title, msg):
    w=WindowsBalloonTip()
    w.show(title, msg)
    time.sleep(10)
    w.close()
    

if __name__ == '__main__':
    balloon_tip("Title for popup", "This is the popup's message")
```
<!-- MARKDOWN-AUTO-DOCS:END -->


