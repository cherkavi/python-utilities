app = tornado.web.Application([(r"/file/([a-zA-Z\-0-9\.:,/_]+)", FileHandler, dict(folder=folder)),])

class FileHandler(tornado.web.RequestHandler):
    def get(self, relative_path):
        print(relative_path)
