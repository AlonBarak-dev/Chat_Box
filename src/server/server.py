import socket
from src.utils.message import Message


class Server:

    def __init__(self):
        # a dict to hold all of the connected clients
        # {"client_name": client_PORT}
        self.clients = {}

        # a list of available ports for new clients
        self.available_ports = [55000 + i for i in range(16)]

        # Create a datagram socket
        self.receive_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # bind the receive socket
        self.server_port = 50000
        self.ip = "localhost"
        self.receive_socket.bind((self.ip, self.server_port))

    def send_response(self, rsp: Message):
        print("hi")

    def listen(self):
        print("hi")

    def connected_response(self, client_name: str):
        rsp = Message("")  # TO DO
        self.send_response(rsp)
        self.listen()

    def connection_failed(self, client_name: str):
        rsp = Message("")  # TO DO
        self.send_response(rsp)
        self.listen()

    def disconnected(self, client_name: str):
        rsp = Message("")  # TO DO
        self.send_response(rsp)
        self.listen()

    def msg_received(self, client_name: str):
        rsp = Message("")  # TO DO
        self.send_response(rsp)
        self.listen()

    def msg_sent(self, client_name: str):
        rsp = Message("")  # TO DO
        self.send_response(rsp)
        self.listen()

    def users_list(self, client_name: str):
        rsp = Message("")  # TO DO
        self.send_response(rsp)
        self.listen()

    def files_list(self, client_name: str):
        rsp = Message("")  # TO DO
        self.send_response(rsp)
        self.listen()

    def downloaded(self, client_name: str):
        rsp = Message("")  # TO DO
        self.send_response(rsp)
        self.listen()
