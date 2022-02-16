import socket
from src.utils.message import Message


class Server:

    def __init__(self):
        # a dict to hold all of the connected clients
        # {"client_name": (client_PORT, client_address)}
        self.clients = {}
        # list of all files located in the server
        self.file_list = []

        # a list of available ports for new clients
        self.available_ports = [55000 + i for i in range(16)]

        # Create a datagram socket
        self.receive_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # bind the receive socket
        self.server_port = 50000
        self.ip = "127.0.0.1"
        self.receive_socket.bind((self.ip, self.server_port))

    def send_response(self, msg: Message):
        """
        this method receive a message that the server prepared to a client and
        responsible for sending the message to the desired client
        :param msg: a message object that contains all the information og the packet
        """
        dest_client = msg.get_receiver()
        dest_tuple = self.clients[dest_client]       # the port of the edge user

        # convert the message object to a string
        msg_bytes = msg.to_string().encode()
        # send the message to the desired client
        self.send_socket.sendto(msg_bytes, dest_tuple)

    def listen(self):
        """
        this method listening to messages from all clients and call the specific function that can handle the
        client request. for example, if the request is a connect type then this method will call
        to the connection response function.
        """

        # listen to a packet from the clients
        msg, address = self.receive_socket.recvfrom(4096)
        # convert the bytes to string
        msg = msg.decode()
        # convert from string to a message object
        msg_obj = Message()
        msg_obj.load(msg)

        # investigate the message request
        msg_type = msg_obj.get_request()

        if msg_type == 'connect':
            self.connected_response(msg_obj)
        elif msg_type == 'disconnect':
            self.disconnected(msg_obj)
        elif msg_type == 'get_user_list':
            self.users_list(msg_obj)
        elif msg_type == 'get_file':
            self.files_list(msg_obj)
        elif msg_type == 'message_request':
            # felt cute, might delete later
            self.msg_received(msg_obj)
            self.msg_sent(msg_obj)
        elif msg_type == 'download':
            self.downloaded(msg_obj)

    def connected_response(self, message: Message):
        """
        this method responsible to connect the client to the server
        base on the request
        :param message: a message object that contain all the information about the request
        :return: true if login successfully, else return false
        """
        # create a response message to be send to the client
        res_msg = Message()

        # initialize the client fields
        client_name_address = str(message.get_sender()).split(',')

        flag = True
        # look for an available port for the client
        if len(self.available_ports) == 0:
            flag = False   # if no available port, login failed
        # initialize the client port and remove from available ports list
        client_port = self.available_ports[0]
        self.available_ports.remove(client_port)
        # set a tuple that contain info about the client
        client_info = (client_port, client_name_address[1])

        self.clients[str(client_name_address[0])] = client_info
        # edit the response message
        res_msg.set_response(res_msg.response_types('connect_response'))
        res_msg.set_sender('server' + ":127.0.0.1")
        res_msg.set_receiver(client_name_address[0])
        res_msg.set_message(flag)

        # send the response message to the client
        self.send_response(res_msg)

    def disconnected(self, message: Message):
        msg = Message("")  # TO DO
        self.send_response(msg)

    def msg_received(self, message: Message):
        msg = Message("")  # TO DO
        self.send_response(msg)

    def msg_sent(self, message: Message):
        msg = Message("")  # TO DO
        self.send_response(msg)

    def users_list(self, message: Message):
        msg = Message("")  # TO DO
        self.send_response(msg)

    def files_list(self, message: Message):
        msg = Message("")  # TO DO
        self.send_response(msg)

    def downloaded(self, message: Message):
        msg = Message("")  # TO DO
        self.send_response(msg)
