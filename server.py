#from socket import AF_INET,SOCK_STREAM,socket
from socket import *

from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Hello! You are using Vchat.Please give your name below first and proceed..", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    try:
        name = None
        name = client.recv(BUFSIZ).decode("utf8")
        if name == "{quit}":
            print("<unkown> has disconnected")
            return 
        print("User name:%s" %name)
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
    except:
        #print("The client would've probably been disconnected!")
        if name:
            print("%s has disconnected - name unknown" %addresses[client], name)
            return
        else:
            print("%s - %s has disconnected" %addresses[client])
            return

    while True:
        try:
            msg = client.recv(BUFSIZ)
        except:
            print("%s - %s has disconnected" %addresses[client], name)
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            
            break
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            try:
                client.send(bytes("{quit}", "utf8"))
            except:
                pass
            del clients[client]
            #client.close()
            #print(*clients)
            print("%s has disconnected" %name)
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf8")+msg)
        except:
            pass

        
clients = {}
addresses = {}

HOST = gethostbyname(gethostname())
PORT = 33000

BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()
