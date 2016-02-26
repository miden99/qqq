import socket

conn = socket.socket()
conn.connect(('localhost', 9090))
conn.send("hello!")
conn = conn.recv(1024)

conn.close()
