import sys
from pgu import gui
import pygame
import threading
import websocket


RESX = 600
RESY = 400
FPS = 40

CONNECT_SUCCESS = False
#


def on_message(ws, message):
    print(message)
    if message != 'Sorry':
        win._quit = True
        main_thread.start()
    else:
        label.value = message
        ws.close()
        # ws = websocket.WebSocketApp("ws://127.0.1.1:8888/websocket", on_message=on_message)
    chat.value += message + '\n'


# Так надо
# def on_open(ws):
#     t2.start()


# Должна отправлять сообщения
def on_btn_send(value):
    mail = input_field.value
    chat.value += mail + '\n'
    ws.send(mail)
    input_field.value = ''


def on_btn_connect(ws):
    ws_thread.start()


# First Window
screen = pygame.display.set_mode((RESX, RESY))

win = gui.Desktop()
win.connect(gui.QUIT, win.quit, None)

#
sign = gui.Table()
Log_in = gui.Input(size=20)
button_connect = gui.Button("Connect")
label = gui.Input(size=20)

# Стол
sign.tr()
sign.td(Log_in)
sign.td(button_connect)
sign.tr()
sign.td(label)
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
