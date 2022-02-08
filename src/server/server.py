import socket


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

    def add_client(self, name):
        if name in self.clients:
            return False
        port = self.get_available_port()
        if port == None:
            return False
        self.clients[name] = port
        return True

    def get_available_port(self):
        # no available ports -> return None
        if self.available_ports is None:
            return None
        # return the first available port number and remove from the list
        port_num = self.available_ports[0]
        self.available_ports.remove(port_num)
        return port_num

    def listen(self):
        print("listening...")
        while True:
            message, address = self.receive_socket.recvfrom(4096)
            message = message.decode()
            """
            TO DO
            msg : <SEQ><NAME><Message>
            """
            seq = message[0]
            name = message[1]       # ignore - expected Name
            content = message[2:]
            # ---------------------------------

            if name not in self.clients:
                """DO SOMETHING"""






            ack_message = "Ack" + seq
            #self.send_socket(ack_message.decode(), )
