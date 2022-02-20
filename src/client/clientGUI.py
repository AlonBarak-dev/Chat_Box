import threading
import tkinter.tix
from tkinter import *
from src.server.server import Server
from src.client.client import Client
import string


class ClientGUI:

    def __init__(self):
        # chat window which is currently hidden
        self.Window = Tk()

        # login button
        self.login_button = Button(self.Window, text="login", command=lambda: self.login())
        self.login_button.place(relx=0.0,
                                rely=0.005)
        # logout button
        self.logout_button = Button(self.Window, text="logout", command=lambda: self.logout())
        self.logout_button["state"] = DISABLED

        # name label
        self.name_label = Label(self.Window,
                                text="name",
                                font="Helvetica 12")
        self.name_label.place(relheight=0.04,
                              relx=0.03,
                              rely=0.0)
        # name input
        self.name_input = Entry(self.Window,
                                font="Helvetica 12")

        self.name_input.place(relwidth=0.05,
                              relheight=0.03,
                              relx=0.06,
                              rely=0.008)
        # adress label
        self.address_label = Label(self.Window,
                                   text="address",
                                   font="Helvetica 12")
        self.address_label.place(relheight=0.04,
                                 relx=0.10,
                                 rely=0.0)
        # address input
        self.address_input = Entry(self.Window,
                                   font="Helvetica 12")

        self.address_input.place(relwidth=0.05,
                                 relheight=0.03,
                                 relx=0.14,
                                 rely=0.008)
        # show online button
        self.show_online_button = Button(self.Window, text="show online", command=lambda: self.show_online())
        self.show_online_button.place(relx=0.2, rely=0.001)
        self.show_online_button["state"] = DISABLED

        # show server files button
        self.show_server_files_button = Button(self.Window, text="show server files",
                                               command=lambda: self.show_server_files())

        self.show_server_files_button.place(relx=0.25, rely=0.001)
        self.show_server_files_button["state"] = DISABLED

        # show chat
        self.display_chat = Text(self.Window,
                                 width=20,
                                 height=2,
                                 font="Helvetica 12",
                                 padx=5,
                                 pady=5)

        self.display_chat.place(relheight=0.645,
                                relwidth=1,
                                rely=0.08)

        # recipient label
        self.recipient_label = Label(self.Window,
                                     text="Send to: (blank to all)",
                                     font="Helvetica 12")

        self.recipient_label.place(relheight=0.05,
                                   relx=0.0001,
                                   rely=0.73)

        # recipient input
        self.recipient_input = Entry(self.Window,
                                     font="Helvetica 12")

        self.recipient_input.place(relwidth=0.1,
                                   relheight=0.03,
                                   relx=0.0001,
                                   rely=0.77)

        # message label
        self.message_label = Label(self.Window,
                                   text="message",
                                   font="Helvetica 12")

        self.message_label.place(relheight=0.05,
                                 relx=0.12,
                                 rely=0.73)

        # message input
        self.message_input = Entry(self.Window,
                                   font="Helvetica 12")

        self.message_input.place(relwidth=0.4,
                                 relheight=0.03,
                                 relx=0.12,
                                 rely=0.77)

        # send button
        self.send_button = Button(self.Window, text="   Send    ",
                                  command=lambda: self.send())

        self.send_button.place(relx=0.6, rely=0.77)
        self.send_button["state"] = DISABLED

        # server file name label
        self.server_file_name_label = Label(self.Window,
                                            text="Server file name:",
                                            font="Helvetica 12")

        self.server_file_name_label.place(relheight=0.05,
                                          relx=0.001,
                                          rely=0.80)

        # server file name input
        self.server_file_name_input = Entry(self.Window,
                                            font="Helvetica 12")

        self.server_file_name_input.place(relwidth=0.1,
                                          relheight=0.03,
                                          relx=0.001,
                                          rely=0.84)

        # save as label
        self.save_as_label = Label(self.Window,
                                   text="File name (Client save as)",
                                   font="Helvetica 12")
        self.save_as_label.place(relheight=0.05,
                                 relx=0.12,
                                 rely=0.80)

        # save as input
        self.save_as_input = Entry(self.Window,
                                   font="Helvetica 14")

        self.save_as_input.place(relwidth=0.1,
                                 relheight=0.03,
                                 relx=0.12,
                                 rely=0.84)

        # download button
        self.download_button = Button(self.Window, text="Download",
                                      command=lambda: self.download())

        self.download_button.place(relx=0.18, rely=0.84)
        self.download_button["state"] = DISABLED

        self.client = None
        self.Window.mainloop()

    def login(self):
        self.client = Client()
        self.client.login(self.name_input.get(), self.address_input.get())
        self.show_online_button["state"] = NORMAL
        self.download_button["state"] = NORMAL
        self.send_button["state"] = NORMAL
        self.show_server_files_button["state"] = NORMAL
        self.login_button["state"] = DISABLED
        self.login_button.place(relx=0.7, rely=0.005)
        self.logout_button["state"] = NORMAL

    def logout(self):
        self.client.logout()

    def show_online(self):
        print("show online")

    def show_server_files(self):
        print("show server files")

    def send(self):
        print("send")

    def download(self):
        print("send")
