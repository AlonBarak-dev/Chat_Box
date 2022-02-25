import socket
import threading
from server import Server
from tkinter import *


class serverGUI:

    def __init__(self):

        # chat window which is currently hidden
        self.Window = Tk()

        self.go = Button(self.Window, text="Start on host", command=lambda: self.start_host())
        self.go.place(relx=0.27,
                      rely=0.15)

        self.go = Button(self.Window, text="Start on localhost", command=lambda: self.start_localhost())
        self.go.place(relx=0.20,
                      rely=0.3)

        host_name = socket.gethostname()
        self.host_add = socket.gethostbyname(host_name)
        self.lable = Label(self.Window, text="Server IP Address : " + self.host_add)

        self.Window.mainloop()

    def start_host(self):
        server = Server(self.host_add)
        server_thread = threading.Thread(target=server.listen2)
        server_thread.start()
        self.lable.place(relx=0.10,
                         rely=0.5)
        print("server is ready..")

    def start_localhost(self):
        server = Server("127.0.0.1")
        server_thread = threading.Thread(target=server.listen2)
        server_thread.start()
        self.lable = Label(self.Window, text="Server IP Address : 127.0.0.1")
        self.lable.place(relx=0.10,
                         rely=0.5)
        print("server is ready..")