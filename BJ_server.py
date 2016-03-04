import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
from Classes.WSHandler import WSHandler


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPool = []

        handlers = [
            (r'/websocket', WSHandler),
        ]

        tornado.web.Application.__init__(self, handlers)


application = Application()

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
