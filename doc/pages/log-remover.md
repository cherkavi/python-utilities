# log-remover

## log remover

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/log-remover/log-remover.py) -->
<!-- The below code snippet is automatically added from ../../python/log-remover/log-remover.py -->
```py
import tornado.ioloop
import tornado.web
import sys
import os


folder = "/var/lib/brand-server/cache/zip"

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        list_of_files = os.listdir(folder)
        counter = 0
        for each_file in list_of_files:
            real_path = os.path.join(folder, each_file)
            if os.path.isfile(real_path):
                os.remove(os.path.join(folder, each_file))
                counter = counter + 1
        self.write("removed: " + str(counter))


def make_app():
    return tornado.web.Application([ (r"/", MainHandler), ])


if __name__ == "__main__":
    if len(sys.argv)<3:
        print("please specify the <port> and <zip folder>")
        sys.exit(2)
    app = make_app()
    app.listen(sys.argv[1])
    folder = sys.argv[2]
    tornado.ioloop.IOLoop.current().start()
```
<!-- MARKDOWN-AUTO-DOCS:END -->


