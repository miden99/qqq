import sys
from pgu import gui
import pygame
import threading
import websocket


RESX = 600
RESY = 400
FPS = 40


#
def on_message(ws, message):
    chat.value += message + '\n'


# Так надо
def on_open(ws):
    t2.start()


# Должна отправлять сообщения
def on_btn_send(value):
    mail = input_field.value
    chat.value += mail + '\n'
    ws.send(mail)
    input_field.value = ''


def on_btn_connect(ws):
    t1.start()

# First Window
screen = pygame.display.set_mode((RESX, RESY))

win = gui.Desktop()
win.connect(gui.QUIT, win.quit, None)

#
sign = gui.Table()
Log_in = gui.Input(size=20)
button_connect = gui.Button("Connect")
label = gui.Label("Мест нет")

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


def login():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            else:
                win.event(event)
        dt = clock.tick(FPS)
        screen.fill((0, 0, 0))
        win.paint()
        pygame.display.flip()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            else:
                app.event(event)
        dt = clock.tick(FPS)
        screen.fill((0, 0, 0))
        app.paint()
        pygame.display.flip()

# Так надо
ws = websocket.WebSocketApp("ws://127.0.1.1:8888/websocket", on_message=on_message,
                                                             on_open=on_open)
# init threads
t1 = threading.Thread(target=ws.run_forever)
t2 = threading.Thread(target=main)

win.run()