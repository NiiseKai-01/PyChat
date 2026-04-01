import socket
import threading

def send_msg(conn):
    while True:
        msg = input("Server: ")
        conn.send(msg.encode())

def recv_msg(conn):
    while True:
        msg = conn.recv(1024)
        print(f"Client {msg.decode()}")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind(("127.0.0.1",55555))
s.listen()
print("server started")

#server side
conn, add = s.accept()
print(f"connected {add}")
t1 = threading.Thread(target=send_msg, args=(conn,))
t2 = threading.Thread(target=recv_msg, args=(conn,))
t1.start()
t2.start()