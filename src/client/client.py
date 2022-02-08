import socket
from src.server import server


class Client:

    def __init__(self, name: str):

        # the name of the client
        self.client_name = name

        # the socket for sending messages to the server
        self.send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_send_address_port = None

        # the socket for receiving messages from the server
        self.receive_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_receive_address_port = None

    def connect(self, server):
        # client cant connect to more than one server
        if self.is_connected():
            print("already connected to a server")
            return False

        # get a free port number from the server
        port = server.get_available_port()

        self.server_send_address_port = (server.ip, server.server_port)
        self.server_receive_address_port = (server.ip, port)
        return True

    def disconnect(self, server):
        # first check if the client is connected to a server, if so disconnect from the server
        if self.is_connected() is True:
            self.server_send_address_port = None
            self.server_receive_address_port = None
            # TO DO
            # server.send("Disconnect {}".format(self.client_name))
            return True
        else:
            return False

    def is_connected(self):
        if self.send_socket.fileno() == -1 and self.receive_socket.fileno() == -1:
            return False
        elif self.send_socket.fileno() != -1 and self.receive_socket.fileno() != -1:
            return True
        else:
            return "ERROR"
