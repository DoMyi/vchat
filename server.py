#from socket import AF_INET,SOCK_STREAM,socket
from socket import *

from threading import Thread

import sys


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        fc = open("connections_log", "a+")
        fc.write("%s:%s has connected.\n" % client_address)
        fc.close()
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
            fc = open("connections_log", "a+")
            fc.write("<unkown> has disconnected\n")
            fc.close()
            return 
        print("User name:%s" %name)
        fc = open("connections_log", "a+")
        fc.write("User name:%s\n" %name)
        fc.close()
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!" % name
        fm = open("messages_log", "a+")
        fm.write("%s has joined the chat!\n" % name)
        fm.close()
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
    except:
        #print("The client would've probably been disconnected!")
        if name:
            print("%s has disconnected - name unknown" %addresses[client], name)
            fc = open("connections_log", "a+")
            fc.write("%s has disconnected - name unknown\n" %addresses[client], name)
            fc.close()
            return
        else:
            print("%s - %s has disconnected" %addresses[client])
            fc = open("connections_log", "a+")
            fc.write("%s - %s has disconnected\n" %addresses[client])
            fc.close()
            return

    while True:
        try:
            msg = client.recv(BUFSIZ)
        except:
            print("%s - %s has disconnected" %addresses[client], name)
            fc = open("connections_log", "a+")
            fc.write("%s has disconnected - " %addresses[client])
            fc.write("%s\n" %name)
            fc.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            fm = open("messages_log", "a+")
            fm.write("%s has left the chat.\n" % name)
            fm.close()
            break
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
            fm = open("messages_log", "a+")
            fm.write(name + ": " + str(msg)[2:-1]+ "\n")
            fm.close()
        else:
            try:
                client.send(bytes("{quit}", "utf8"))
            except:
                pass
            del clients[client]
            #client.close()
            #print(*clients)
            print("%s has disconnected" %name)
            fc = open("connections_log", "a+")
            fc.write("%s has disconnected\n" %name)
            fc.close()
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            fm = open("messages_log", "a+")
            fm.write("%s has left the chat.\n" % name)
            fm.close()
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

#log files

try:
    if __name__ == "__main__":
        SERVER.listen(5)
        fc = open("connections_log", "a+")
        fc.write("="*70 + "\n")
        fc.close()
        fm = open("messages_log", "a+")
        fm.write("="*70 + "\n")
        fm.close()
        print("Waiting for connection...")
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        #fc.write("="*70)
        #fm.write("="*70)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
except KeyboardInterrupt:
    SERVER.close()
    fc.close()
    fm.close()
    sys.exit()
