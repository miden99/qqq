import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPool = []

        # settings = {
        # 'static_url_prefix': '/static/',
        # }
        # connection = pymongo.Connection('127.0.0.1', 27017)
        # self.db = connection.chat
        handlers = [
            # (r'/', WSHandler),
            (r'/websocket', WSHandler),
        ]

        tornado.web.Application.__init__(self, handlers)


class WSHandler(tornado.websocket.WebSocketHandler):
    # Добавляет в список новые подключения
    def open(self):
        print('new connection')
        self.application.webSocketsPool.append(self)
        print(self.application.webSocketsPool)

    # Отсылает сообщения другим клиентам и сообщает об отправке
    def on_message(self, message):
        # print('message received:  %s' % message)
        # print('send -->', message)
        # self.ws_connection.write_message(message)
        for value in self.application.webSocketsPool:
            if value != self:
                print('send -->', message)
                value.ws_connection.write_message(message)
            else:
                self.ws_connection.write_message("ping")

    # Удаляет из списка отключившиеся клинты
    def on_close(self):
        print('connection closed')
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]

    # def check_origin(self, origin):
    #     return True


# application = tornado.web.Application([
#     (r'/websocket', WSHandler),
# ])
application = Application()

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
