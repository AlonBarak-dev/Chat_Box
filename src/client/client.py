import socket
from src.server import server
from src.utils.message import Message


class Client:

    def __init__(self, name: str):
        # the name of the client
        self.client_name = name

        # the socket for sending messages to the server
        self.send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_send_address_port = ("127.0.0.1", 55000)   # the server port

        # the socket for receiving messages from the server
        self.receive_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_receive_address_port = None

    def send_msg(self, message: Message):

        msg_str = message.to_string()       # felt cute, might delete later

    def listen(self):
        print("hi")

    def get_port(self):
        """
        this method request the server for the given receive port
        :return: the port number
        """
        msg = Message("<port><{}>".format(self.client_name))
        self.send_msg(msg)
        self.server_receive_address_port = ("127.0.0.1", self.listen())

    def login(self):
        """
        this method responsible for the login process.
        """
        msg = Message("<connect><{}>".format(self.client_name))  # create a new message object
        self.send_msg(msg)
        self.get_port()
        self.listen()

    def logout(self):
        """
        this method allows the users to logout from the server by disconnecting them from the server
        :return:
        """
        msg = Message("<disconnect><{}>".format(self.client_name))
        self.send_msg(msg)
        self.listen()

    def get_users_list(self):
        """
        this method request from the server the list of all active clients at the moment
        :return:
        """
        msg = Message("<users_list><{]>".format(self.client_name))
        self.send_msg(msg)
        self.listen()

    def private_msg(self, message : str, dest : str):
        """
        this method request from the server to send a private message to a specific client on the system
        :param message: the message the client want to send to the destination
        :param dest: another user's name
        :return:
        """

        msg = Message("<private_msg><{}><{}><{}>".format(message, self.client_name, dest))
        self.send_msg(msg)
        self.listen()

    def public_msg(self, message : str):
        """
        this method allows the user to send a public message to all of the user connected to the
        system at the current moment.
        :param message: the message the client want to send to the users
        :return:
        """

        msg = Message("<public_msg><{}><{}>".format(message, self.client_name))
        self.send_msg(msg)
        self.listen()

    def get_files_list(self):
        """
        this method allows the user to ask for a list of all the files
        stored n the server and later on choose a file from this list
        and download it
        :return:
        """
        msg = Message("<files_list><{}>".format(self.client_name))
        self.send_msg(msg)
        self.listen()

    def download(self, file_name : str):
        """
        this method allows the user to download a file from the file list.
        :param file_name:
        :return:
        """
        msg = Message("<download><{}><{}>".format(file_name, self.client_name))
        self.send_msg(msg)
        self.listen()
