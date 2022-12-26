## https://docs.cherrypy.dev/en/latest/tutorials.html
## #webframework
# pip3 install cherrypy
# python3 cherry.py

# ❯ curl -v -X POST localhost:8080 -H "Content-Length:0"
#        < Set-Cookie: session_id=e0f93af0d8aab14b06d80c9152a5c78bbf9fa3a8; expires=Sun, 25 Dec 2022 20:34:08 GMT; Max-Age=3600; Path=/
#        A17b385F
# ❯ curl -X GET localhost:8080 -H "Cookie: session_id=e0f93af0d8aab14b06d80c9152a5c78bbf9fa3a8"
#        A17b385F


import random
import string

import cherrypy


@cherrypy.expose
class StringGeneratorWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']

    def POST(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(StringGeneratorWebService(), '/', conf)
