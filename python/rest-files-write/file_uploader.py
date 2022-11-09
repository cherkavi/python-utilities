import tornado.web
import tornado.ioloop

MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB

MAX_STREAMED_SIZE = 1 * GB


# curl -X PUT -H "Content-Type: application/jpg" -H "x-username: cherkavi" -d @uploader-local.png http://127.0.0.1:7777

@tornado.web.stream_request_body
class MainHandler(tornado.web.RequestHandler):

    def initialize(self):
        print("start upload")

    def prepare(self):
        self.f = open("/tmp/test.png", "wb")
        # dict(self.request.headers)['X-Username']
        self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)

    def post(self):
        print("upload completed")
        self.f.flush()
        self.f.close()

    def put(self):
        print("upload completed")
        self.f.flush()
        self.f.close()

    def data_received(self, data):
        print("write: %d " % len(data))
        self.f.write(data)

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()