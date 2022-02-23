import threading
from tkinter import *
from client import Client


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
                                      command=lambda: self.download_thread())

        self.download_button.place(relx=0.18, rely=0.84)
        self.download_button["state"] = DISABLED

        self.proceed_button = Button(self.Window, text="Proceed", command=lambda: self.proceed_thread())
        self.proceed_button.place(relx=0.30, rely= 0.84)
        self.proceed_button["state"] = DISABLED

        self.update_button = Button(self.Window, text="Update screen", command=lambda: self.check_msg())
        self.update_button.place(relx=0.7, rely=0.90)

        self.client = None
        self.Window.mainloop()

    def login(self):
        self.client = Client()

        if self.client.login(self.name_input.get(), self.address_input.get()):
            self.show_online_button["state"] = NORMAL
            self.download_button["state"] = NORMAL
            self.send_button["state"] = NORMAL
            self.show_server_files_button["state"] = NORMAL
            self.login_button["state"] = DISABLED
            self.logout_button.place(relx=0.5, rely=0.005)
            self.logout_button["state"] = NORMAL
            self.display_chat.insert(END, "Welcome, " + self.client.client_name + "\n")

    def check_msg(self):
        print(len(self.client.msg_dict['message_received']))
        while len(self.client.msg_dict['message_received']) != 0:
            self.display_chat.insert(END, self.client.msg_dict['message_received'].pop() + "\n")

    def logout(self):
        self.client.logout()
        self.login_button["state"] = NORMAL
        self.display_chat.insert(END, "\nGood Bye, " + self.client.client_name + "\n")
        self.logout_button["state"] = DISABLED
        self.show_online_button["state"] = DISABLED
        self.download_button["state"] = DISABLED
        self.send_button["state"] = DISABLED
        self.show_server_files_button["state"] = DISABLED
        self.logout_button.place(relx=0.0, rely=0.005)

    def show_online(self):
        users_list = self.client.get_users_list()
        i = len(users_list) - 1
        self.display_chat.insert(END, "\n-----USERS-----\n")
        while i >= 0:
            self.display_chat.insert(END, users_list[i] + ", ")
            i -= 1
        self.display_chat.insert(END, "\n-----USERS-----\n")

    def show_server_files(self):
        files_list = self.client.get_files_list()
        i = len(files_list) - 1
        self.display_chat.insert(END, "\n-----FILES-----\n")
        while i >= 0:
            self.display_chat.insert(END, files_list[i] + ", ")
            i -= 1
        self.display_chat.insert(END, "\n-----FILES-----\n")

    def send(self):

        # get the user name from the GUI in case the client wants to send a privet message.
        # will be None if he wants Broadcast message
        user_name = self.recipient_input.get()
        message = self.message_input.get()
        flag = True
        if user_name == "":
            # broadcast message it is
            flag = self.client.public_msg(message)
        else:
            flag = self.client.private_msg(message=message, dest=user_name)
            if flag:
                self.display_chat.insert(END, self.client.client_name + ": private : " + user_name + " : " + message
                                         + "\n")
        if not flag:
            self.display_chat.insert(END, self.client.client_name +
                                     ": message failed to reach its target.. try again\n")

    def download_thread(self):
        file_name = self.server_file_name_input.get()
        new_file_name = self.save_as_input.get()
        self.proceed_button["state"] = NORMAL
        thread = threading.Thread(target=self.download, args=(file_name, new_file_name,))
        thread.start()
        thread2 = threading.Thread(target=self.check_process, args=(file_name,))
        thread2.start()

    def download(self, file_name: str, new_file_name: str):
        self.display_chat.insert(END, "\n Got a download connection\n")
        if self.client.download(file_name, new_file_name):
            self.display_chat.insert(END, "\n file: " + file_name + " was downloaded successfully!\n")
        else:
            self.display_chat.insert(END, "\n file: " + file_name + " doesn't exist!\n")

    def proceed_thread(self):
        thread = threading.Thread(target=self.proceed)
        thread.start()

    def proceed(self):
        self.client.msg_dict["proceed_messages"].pop()
        self.proceed_button["state"] = DISABLED

    def check_process(self, file_name: str):
        while len(self.client.msg_dict["proceed_messages"]) == 0:
            continue
        self.display_chat.insert(END, "\n file: " + file_name + " was downloaded partly, please press Proceed"
                                                                "to resume the download process\n"
                                                                "Last Byte is: " +
                                 str(self.client.msg_dict["proceed_messages"][0]) + "\n")