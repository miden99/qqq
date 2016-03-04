import tornado.websocket
from Classes.Client import Client
import json


class WSHandler(tornado.websocket.WebSocketHandler):
    # Добавляет в список новые подключения
    def open(self):
        if len(self.application.webSocketsPool) < 2:
            print('new connection')
            self.application.webSocketsPool.append(self)
            print(self.application.webSocketsPool)
            self.ws_connection.write_message('Welcome')
        else:
            self.ws_connection.write_message('Sorry')
            print('sorry')

    def on_message(self, message):
        """
        Отсылает сообщения другим клиентам и сообщает об отправке
        :param message: flgjfdjgfdj
        """
        message = json.loads(message)
        print("message --> ", type(message))
        for value in self.application.webSocketsPool:
            if value != self:
                print('send -->', message)
                value.ws_connection.write_message(message)

    def on_close(self):
        """
        Удаляет из списка отключившиеся клиенты
        :return:
        """
        print('connection closed')
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]
