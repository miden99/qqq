import sys
from pgu import gui
import pygame
import threading
import websocket
import json

RESX = 600
RESY = 400
FPS = 40

CONNECT_SUCCESS = False
#


# class App(websocket.WebSocketApp):
#     def send(self, data, opcode=0x1):
#         super().send(data, opcode=opcode)


def on_message(ws, message):
    print(type(message))
    if message != 'Sorry':
        win._quit = True
        main_thread.start()
        login = input_login.value
        message = {"login": login}
        # message = "Exit"
        ws.send(json.dumps(message))
        ws.send(message)
    else:
        input_error.value = message
        ws.close()
        # ws = websocket.WebSocketApp("ws://127.0.1.1:8888/websocket", on_message=on_message)
    # chat.value += message + '\n'


# Должна отправлять сообщения
def on_btn_send(value):
    mail = input_field.value
    chat.value += mail + '\n'
    ws.send(mail)
    input_field.value = ''


def on_btn_connect(btn_event):
    ws_thread.start()
    login = input_login.value



# First Window
screen = pygame.display.set_mode((RESX, RESY))

win = gui.Desktop()
win.connect(gui.QUIT, win.quit, None)

#
sign = gui.Table()
label_login = gui.Label("nick")
label_error = gui.Label("error")
input_login = gui.Input(size=20)
button_connect = gui.Button("Connect")
input_error = gui.Input(size=20)

# Стол
sign.tr()
sign.td(label_login)
sign.td(input_login)
sign.td(button_connect)
sign.tr()
sign.td(label_error)
sign.td(input_error)
button_connect.connect(gui.CLICK, on_btn_connect, "Connect")


win.init(widget=sign)

# INIT


# Second Window
app = gui.Desktop()
app.connect(gui.QUIT, app.quit, None)

# SOCKETS

button_send = gui.Button('Send message')
grid = c = gui.Table()
input_field = gui.Input(size=20)
chat = gui.TextArea()
button_quit = gui.Button("Quit")

# Размер чата
chat.style.height = 200
chat.style.width = 300

# Стол
grid.tr()
grid.td(input_field)
grid.tr()
grid.td(chat)
grid.tr()
grid.td(button_send)

button_send.connect(gui.CLICK, on_btn_send, "Send")
app.init(widget=grid)
clock = pygame.time.Clock()


def main():
    done = True
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("!!")
                done = False
                ws.close()
                break
            else:
                app.event(event)

        dt = clock.tick(FPS)
        screen.fill((0, 0, 0))
        app.paint()
        pygame.display.flip()

# Так надо
ws = websocket.WebSocketApp("ws://127.0.1.1:8888/websocket", on_message=on_message)
# init threads
ws_thread = threading.Thread(target=ws.run_forever)
main_thread = threading.Thread(target=main)

win.run()
