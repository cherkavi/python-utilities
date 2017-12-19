#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import datetime

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.set_header('Content-Type', 'application/text')
        self.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.finish()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
