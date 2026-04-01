import socket
import threading
import sys

# def send_msg(client):
#     while True:
#         msg = input("Client: ")
#         client.send(msg.encode())
def recv_msg(client):
    while True:
        msg = client.recv(1024)
        sys.stdout.write("\r\033[K")
        sys.stdout.write(f"Server: {msg.decode()}\n")
        sys.stdout.write("Client: ")
        sys.stdout.flush()


        
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("192.168.1.101",55555))

#client side
# t1=threading.Thread(target=send_msg, args=(client,))
t2=threading.Thread(target=recv_msg, args=(client,), daemon=True)
# t1.start()
t2.start()

while True:
    msg = input(f"Client: ")
    client.send(msg.encode())