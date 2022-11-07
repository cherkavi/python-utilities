#!/usr/bin/env python
import tornado.escape
import tornado.web
import tornado.ioloop
import time
import sys

class GetCurrentTimestamp(tornado.web.RequestHandler):
	def get(self):
		response=time.strftime("%Y%m%d%H%M%S")
		self.write(response)

application=tornado.web.Application([(r"/",GetCurrentTimestamp),])

if __name__=="__main__":
	if len(sys.argv)>1:
		application.listen(sys.argv[1])
	else:
		application.listen(9993)
	tornado.ioloop.IOLoop.instance().start()

