import os
import time
import subprocess
from datetime import datetime 
import tornado.ioloop
import tornado.web
import threading


def clear_binary_line(b_line):
    next_line = b_line.decode('utf-8')
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    index = next_line.rfind("/")
    if index >= 0:
        next_line = next_line[index+1:]
    return next_line


def execute_sql_script(command):
    try:
        process = subprocess.Popen( command, stdout = subprocess.PIPE )
        result = False
        for b_line in process.stdout:
            line = clear_binary_line(b_line)
            if result == True:
                return int(line.strip())
            if line.find("-------") >= 0:
                result = True
    finally:
        process.stdout.close()
    return result


def execute_script(command):
    subprocess.Popen( command )


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, holder):
        self.holder = holder

    def get(self):
        self.write("last update: " + str(self.holder.last_update))


class ResultHolder():
    def __init__(self):
        self.last_update = ""


def startTornadoInstance():
    tornado.ioloop.IOLoop.instance().start()

def startTornado(holder):
    application = tornado.web.Application([(r"/", MainHandler, dict(holder=holder)),])
    application.listen(9867)
    threading.Thread(target=startTornadoInstance).start()

def stopTornado():
    tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    try:    
        result_holder = ResultHolder()
        startTornado(result_holder)
        while True:
            result_holder.last_update = datetime.now()
            print(">>>", result_holder.last_update)
            if execute_sql_script("db-query.bat")>0:
                execute_script("slack.bat")
                break
            time.sleep(60)
    finally:
        stopTornado()
