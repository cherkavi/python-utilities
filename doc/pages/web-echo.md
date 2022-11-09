# web-echo

## echo ssl

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/web-echo/echo-ssl.py) -->
<!-- The below code snippet is automatically added from ../../python/web-echo/echo-ssl.py -->
```py
#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import datetime
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.set_header('Content-Type', 'application/text')
        with open("/home/projects/python-utilities/web-echo/out.txt", "a") as output:
            output.write(f">>> GET request {self.get_argument('arg1','')} \n")
        self.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.finish()

    def post(self):
        data = self.get_argument('body', 'No data received')
        with open("/home/projects/python-utilities/web-echo/out.txt", "a") as output:
            output.write(f">>> POST request:  {data} \n")
        self.write(data)
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    # sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    # -keyout cherkavideveloper.pem -out cherkavideveloper.pem \
    # -subj "/C=DE/ST=Bavaria/L=München/O=cherkavi/CN=cherkavi developer"

    http_server = tornado.httpserver.HTTPServer(app, ssl_options={"certfile": "/home/projects/temp/ssl-custom/cherkavideveloper.pem", "keyfile": "/home/projects/temp/ssl-custom/cherkavideveloper.pem"})
    http_server.listen(443)
    tornado.ioloop.IOLoop.instance().start()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## echo

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/web-echo/echo.py) -->
<!-- The below code snippet is automatically added from ../../python/web-echo/echo.py -->
```py
#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import datetime

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.set_header('Content-Type', 'application/text')
        self.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.finish()

    def post(self):
        data = self.get_argument('body', 'No data received')
        self.write(data)
        self.finish()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
```
<!-- MARKDOWN-AUTO-DOCS:END -->


