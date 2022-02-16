import socket
from src.utils.message import Message


class Client:

    def __init__(self):
        # the name of the client
        self.client_name = None
        self.client_address = None

        # server port
        self.server_port = 50000

        # the socket for sending messages to the server
        self.send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_send_address_port = ("127.0.0.1", self.server_port)  # the server port

        # the socket for receiving messages from the server
        self.receive_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_receive_address_port = None

        # false if doesnt connected to a server, True if does
        self.connected = False

    def send_msg(self, message: Message):

        msg_str = message.to_string()  # felt cute, might delete later
        self.send_socket.sendto(msg_str.encode(), self.server_send_address_port)

    def listen(self) -> Message:
        """
        this method listens to the server and translate the server's response into Message Objects
        :return: Message object
        """
        # receive the response packet from the server
        msg, address = self.receive_socket.recvfrom(4096)
        msg = msg.decode()
        res_msg = Message()
        res_msg.load(msg)
        return res_msg

    def update_port(self, msg_login: Message):
        """
        this method request the server for the given receive port
        :return: the port number
        """
        port = msg_login.get_message()
        if port != 0:
            # connect the client and the server with a socket
            self.server_receive_address_port = (self.client_address, port)
            self.receive_socket.bind(self.server_receive_address_port)
        return port

    def login(self, name: str, address: str):
        """
        this method responsible for the login process.
        return: true if connected, false otherwise
        """
        # initialize both client's name and address
        self.client_name = name
        self.client_address = address
        # create a packet to send to the server
        msg = Message()
        msg.set_request(msg.request_types('connect'))
        msg.set_sender(self.client_name + "," + self.client_address)

        # send the message to the server
        self.send_msg(msg)
        # listen to the server response
        login_response = self.listen()
        # check if the connection were successful or not
        if self.update_port(login_response) == 0:
            return False
        self.connected = True
        return True

    def logout(self):
        """
        this method allows the users to logout from the server by disconnecting them from the server
        :return: true if disconnected, false otherwise
        """
        # create a message to disconnect from the server
        msg = Message()
        msg.set_request(msg.request_types('disconnect'))
        msg.set_sender(self.client_name + "," + self.client_address)

        # send the message to the server
        self.send_msg(msg)
        # listen to the response from the server
        response_msg = self.listen()
        response_msg = response_msg.get_message()
        # if the logout process was successful then disconnect from the server and return true
        # else, return False
        if response_msg is True:
            self.server_receive_address_port = None
            self.connected = False  # disconnect from the server
            return True
        return False

    def get_users_list(self):
        """
        this method request from the server the list of all active clients at the moment
        :return: a list of strings -> ["name1","name2",....,"nameN"]
        """
        # create a message asking for the list of all active users
        msg = Message()
        msg.set_request(msg.set_request('get_user_list'))
        msg.set_sender(self.client_name + "," + self.client_address)

        # send the message to the server
        self.send_msg(msg)
        # listen to the response from the server
        response_msg = self.listen()
        # extract the message content from the packet
        response_msg = response_msg.get_message()
        # "<name1><name2><name3>....<nameN>" is the input for extract_list function
        user_list = self.extract_list(response_msg)
        # return the users list
        return user_list

    def private_msg(self, message: str, dest: str):
        """
        this method request from the server to send a private message to a specific client on the system
        :param message: the message the client want to send to the destination
        :param dest: another user's name
        :return: true if the message sent successfully , false if faced issues
        """

        # create a message that request the server to send a private message to a specific user
        msg = Message()
        msg.set_request(msg.request_types('message_request'))
        msg.set_sender(self.client_name + "," + self.client_address)
        msg.set_receiver(dest)
        msg.set_message(message)

        # send the message to the server
        self.send_msg(msg)
        # listen to the server response
        response_msg = self.listen()
        # return true if sent, false if not
        response_msg = response_msg.get_message()
        return response_msg

    def public_msg(self, message: str):
        """
        this method allows the user to send a public message to all of the user connected to the
        system at the current moment.
        :param message: the message the client want to send to the users
        :return: true if the message sent successfully , false if faced issues
        """

        # create a message that request the server to send a message to all users connected
        msg = Message()
        msg.set_request(msg.request_types('message_request'))
        msg.set_sender(self.client_name + "," + self.client_address)
        msg.set_receiver('all')
        msg.set_message(message)

        # send the packet to the server
        self.send_msg(msg)
        # listen to server response
        response_msg = self.listen()
        # return true if sent, false if not
        response_msg = response_msg.get_message()
        return response_msg

    def get_files_list(self):
        """
        this method allows the user to ask for a list of all the files
        stored n the server and later on choose a file from this list
        and download it
        :return: a list of strings
        """

        # create a message that request a list of all files located in the server
        msg = Message()
        msg.set_request(msg.request_types('get_file'))
        msg.set_sender(self.client_name + "," + self.client_address)

        # send the packet to the server
        self.send_msg(msg)
        # listen to the response from the server
        response_msg = self.listen()

        # extract the list from the message
        response_msg = response_msg.get_message()
        files_list = self.extract_list(response_msg)
        return files_list

    def download(self, file_name: str):
        """
        this method allows the user to download a file from the file list.
        :param file_name:
        :return: ture if the file fully downloaded, false if failed
        """

        # create a message that request to download a file from the server
        msg = Message()
        msg.set_request(msg.request_types('download'))
        msg.set_sender(self.client_name + "," + self.client_address)
        msg.set_message(file_name)

        # send the message to the server
        self.send_msg(msg)
        # listen to the server response
        response_msg = self.listen()
        # still not perfect, might change later
        response_msg = response_msg.get_message()
        return response_msg

    def extract_list(self, message: str) -> list:
        """
        this method receive a string of users/files and extract a list from it
        by parsing the string name by name.
        :param message: "<name1><name2><name3>....<nameN>" is the input for extract_list function
        :return: a list of strings -> ["name1","name2",....,"nameN"]
        """
        users_list = []
        users_list = message[1:-2].split("><")
        return users_list
