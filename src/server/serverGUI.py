import threading
from server import Server
from tkinter import *


class serverGUI:

    def __init__(self):

        # chat window which is currently hidden
        self.Window = Tk()

        self.go = Button(self.Window, text="Start", command=lambda: self.start())
        self.go.place(relx=0,
                      rely=0)

        self.Window.mainloop()


    def start(self):
        server = Server()
        server_thread = threading.Thread(target=server.listen)
        server_thread.start()