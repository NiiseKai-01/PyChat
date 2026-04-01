#server_side

import socket
import threading

host = "127.0.0.1"
port = 55555
clients = []
nicknames = []


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen()
print("server is listening")

def broadcast(message):
    for client in clients:
        client.send(message.encode())

def handle(client):
    while True:
       try:
           msg = client.recv(1024).decode()
           broadcast(msg)
       except:
           if client in clients:
            i = clients.index(client)
            clients.remove(client)
            client.close()
            nname = nicknames[i]
            nicknames.remove(nname)
            broadcast(f"{nname} left the chat!")

def receive():
    while True:
        client,addr = s.accept()
        print(f"Connected to {client}, add={addr}")
        clients.append(client)

        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        broadcast(f"{nickname} joined the server!")

        hthread =  threading.Thread(target=handle, args=(client,))
        hthread.start()

receive()  