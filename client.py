

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sys



def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        top.quit()
        client_socket.close()
        top.destroy()
        sys.exit(0)


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    try:
        client_socket.send(bytes("{quit}", "utf8"))
        client_socket.close()
    except:
        top.destroy()
        sys.exit(0)
    top.destroy()
    

top = tkinter.Tk()

top.title("Vchat")

messages_frame = tkinter.Frame(top,width=590,height=300)

#messages_frame.pack(side="top", fill="both", expand=1)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("  ")
scrollbar = tkinter.Scrollbar(messages_frame)  # adding a scrollbar
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
img=tkinter.PhotoImage("/images/back.png")
background_label = tkinter.Label(top, image=img)
background_label.pack()
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
#top.mainloop()

#Connecting to the server -->may not work if server isn't active..
HOST = input("Enter host:")
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() # Starts GUI execution.
