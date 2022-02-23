import socket
import threading
from server import Server
from tkinter import *


class serverGUI:

    def __init__(self):

        # chat window which is currently hidden
        self.Window = Tk()

        self.go = Button(self.Window, text="Start", command=lambda: self.start())
        self.go.place(relx=0.45,
                      rely=0.2)
        host_name = socket.gethostname()
        host_add = socket.gethostbyname(host_name)
        self.lable = Label(self.Window, text="Server IP Address : " + host_add)
        self.lable.place(relx=0.10,
                         rely= 0.5)

        self.Window.mainloop()

    def start(self):
        server = Server()
        server_thread = threading.Thread(target=server.listen2)
        server_thread.start()
        print("server is ready..")