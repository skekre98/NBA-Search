import socket
import threading
Host = ''
Port = 25565

def background1():
    while True:
        Hello1 = conn1.recv(1024)
        print(Hello1.decode())
        conn2.send(Hello1)
def background2():
    while True:
        Hello2 = conn2.recv(1024)
        print(Hello2.decode())
        conn1.send(Hello2)

def GetUser(Messager):
    print("Looking for connection")
    conn, address = Messager.accept()
    Username = conn.recv(1024)
    Username = Username.decode()
    print("Found a connection " + str(address[0]) + " with username " + Username)
    return conn, address, Username

Messager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Messager.bind((Host,Port))
Messager.listen(2)
conn1, address1, Username1 = GetUser(Messager)
conn2, address2, Username2 = GetUser(Messager)

threading1 = threading.Thread(target=background1)
threading1.start()

threading2 = threading.Thread(target=background2)
threading2.start()