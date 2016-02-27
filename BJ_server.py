import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPool = []

        handlers = [
            (r'/websocket', WSHandler),
        ]

        tornado.web.Application.__init__(self, handlers)


class WSHandler(tornado.websocket.WebSocketHandler):
    # Добавляет в список новые подключения
    def open(self):
        if len(self.application.webSocketsPool) < 2:
            print('new connection')
            self.application.webSocketsPool.append(self)
            print(self.application.webSocketsPool)
        else:
            self.ws_connection.write_message('Sorry')
            print('sorry')

    # Отсылает сообщения другим клиентам и сообщает об отправке
    def on_message(self, message):
        # print('message received:  %s' % message)
        # print('send -->', message)
        # self.ws_connection.write_message(message)
        for value in self.application.webSocketsPool:
            if value != self:
                print('send -->', message)
                value.ws_connection.write_message(message)
            # else:
                # self.ws_connection.write_message("ping")

    # Удаляет из списка отключившиеся клиенты
    def on_close(self):
        print('connection closed')
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]


application = Application()

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
