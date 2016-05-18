import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import define, options
import logging

from urls import urls
from settings import settings
# import apps.main.views

define("port", default=9091, help="run on the given port", type=int)

print '\n\ninvoking server.py'


class Application(tornado.web.Application):
    print '\n\ninvoked Application()\n'

    def __init__(self):
        print '\ninside Application __init__()'
        tornado.web.Application.__init__(self, urls, **settings)
        print 'Aapplication __init__ caleed with web.Application()'
        print 'returning from Application __init__'


def main():
    tornado.options.parse_command_line()
    print '\ncreating app=Applicatoin()'
    app = Application()
    print '\napp= Aapplication() created -> app : ', app
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print "\nStarting server on http://127.0.0.1:%s" % options.port

    try:

        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print '\n\nEXCEPTION KEYBOARDINTERRUPT INITIATED\n'
        print "Stopping Server....\n"
        print 'closing all websocket connections objects and corresponsding pika client objects\n'
        # wsparticipants = apps.main.views.websocketParticipants
        # for ws in wsparticipants:
        #     print '\nCLOSING WS.on_close object : ', ws
        #     ws.on_close()

        # apps.main.views.websocketParticipants = []
        print "\nServer Stopped.\n"


if __name__ == "__main__":
    main()
