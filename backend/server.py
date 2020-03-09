from endpoints import *
from tornado.ioloop import IOLoop
from tornado.web import Application
import tornado.httpserver

TORNADO_PORT = 5555
TORNADO_DEBUG = True


class FuberBackend:
    def __init__(self):
        self.application = self.start_tornado()

        server = tornado.httpserver.HTTPServer(self.application)
        server.bind(TORNADO_PORT)
        server.start(1)
        IOLoop.current().start()

    def start_tornado(self):
        urls = [
            (r"/login", LoginHandler),
            (r"/locate", LocateHandler),
            (r"/book", BookHandler),
            (r"/notif", NotifHandler),
        ]

        app = Application(urls, debug=TORNADO_DEBUG)

        return app


if __name__ == '__main__':
    service = FuberBackend()
