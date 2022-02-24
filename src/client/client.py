import os
import socket
import threading
import time

from message import Message


class Client:

    def __init__(self):
        # the name of the client
        self.client_name = None
        self.client_address = None

        # server port
        self.server_port = 50000

        # the socket for receiving messages from the server
        self.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # the socket for file transfer
        self.server_download_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # default values
        self.server_address = '127.0.0.1'
        self.server_address_port = (self.server_address, self.server_port)

        # false if doesnt connected to a server, True if does
        self.connected = False
        self.listener = False
        self.msg_listen = threading.Thread(target=self.listen_msg)
        self.msg_dict = {
            'connect_response': [],
            'disconnect_response': [],
            'user_list': [],
            'file_list': [],
            'message_response': [],
            'message_received': [],
            'download_response': [],
            'proceed_messages': []
        }


    def send_msg(self, message: Message):

        msg_bytes = message.to_string().encode()  # felt cute, might delete later
        self.server_socket.send(msg_bytes)

    def listen_msg(self):
        """
        this method listen only to broadcast/private messages and inform the client in case there are new messages
        """
        while True:
            # receive the response packet from the server
            msg = self.server_socket.recv(65536)
            msg = msg.decode()
            res_msg = Message()
            res_msg.load(msg)
            print("Message: " + res_msg.to_string() + "\n")
            if res_msg.get_response() == 'connect_response':
                self.msg_dict['connect_response'].append(res_msg)
            elif res_msg.get_response() == 'disconnect_response':
                self.msg_dict['disconnect_response'].append(res_msg)
            elif res_msg.get_response() == 'user_list':
                self.msg_dict['user_list'].append(res_msg)
            elif res_msg.get_response() == 'file_list':
                self.msg_dict['file_list'].append(res_msg)
            elif res_msg.get_response() == 'message_response':
                self.msg_dict['message_response'].append(res_msg)
            elif res_msg.get_response() == 'message_received':
                message = self.msg_received(res_msg.get_sender(), res_msg)
                self.msg_dict['message_received'].append(message)
            elif res_msg.get_response() == 'download_response':
                self.msg_dict['download_response'].append(res_msg)

    def login(self, name: str, address: str):
        """
        this method responsible for the login process.
        return: true if connected, false otherwise
        """

        # initialize both client's name and address
        self.client_name = name
        self.server_address_port = (address, self.server_port)
        self.server_address = address
        # create a packet to send to the server
        msg = Message()
        msg.set_request('connect')
        msg.set_sender(self.client_name)

        # connect to the server
        self.server_socket.connect(self.server_address_port)
        self.msg_listen.start()

        # send the message to the server
        self.send_msg(msg)

        # listen to the server response
        while len(self.msg_dict['connect_response']) == 0:
            continue

        login_response = self.msg_dict['connect_response'].pop()

        self.connected = True
        return login_response.get_message()

    def logout(self):
        """
        this method allows the users to logout from the server by disconnecting them from the server
        :return: true if disconnected, false otherwise
        """
        # create a message to disconnect from the server
        msg = Message()
        msg.set_request('disconnect')
        msg.set_sender(self.client_name)

        # send the message to the server
        self.send_msg(msg)
        # listen to the response from the server

        while len(self.msg_dict['disconnect_response']) == 0:
            continue
        response_msg = self.msg_dict['disconnect_response'].pop()

        response_msg = response_msg.get_message()
        # if the logout process was successful then disconnect from the server and return true
        # else, return False
        if response_msg is True:
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
        msg.set_request('get_user_list')
        msg.set_sender(self.client_name)

        # send the message to the server
        self.send_msg(msg)
        # listen to the response from the server
        while len(self.msg_dict['user_list']) == 0:
            continue
        response_msg = self.msg_dict['user_list'].pop()
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
        msg.set_request('message_request')
        msg.set_sender(self.client_name)
        msg.set_receiver(dest)  # assuming its a name of a client
        msg.set_message(message)
        # send the message to the server
        self.send_msg(msg)
        # listen to the server response
        while len(self.msg_dict['message_response']) == 0:
            continue
        response_msg = self.msg_dict['message_response'].pop()
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
        msg.set_request('message_request')
        msg.set_sender(self.client_name)
        msg.set_receiver('all')
        msg.set_message(message)

        # send the packet to the server
        self.send_msg(msg)
        # listen to server response
        while len(self.msg_dict['message_response']) == 0:
            continue
        response_msg = self.msg_dict['message_response'].pop()
        # return true if sent, false if not
        response_msg = response_msg.get_message()
        return response_msg
        # return True

    def msg_received(self, src: str, message: Message):
        """
        this method is responsible to inform the client he has a new message from another user
        :param message: the message that the client received
        :param src: the source of the message
        :return:
        """
        return src + ": " + message.get_message()

    def get_files_list(self):
        """
        this method allows the user to ask for a list of all the files
        stored n the server and later on choose a file from this list
        and download it
        :return: a list of strings
        """

        # create a message that request a list of all files located in the server
        msg = Message()
        msg.set_request('get_file')
        msg.set_sender(self.client_name)

        # send the packet to the server
        self.send_msg(msg)
        # listen to the response from the server
        while len(self.msg_dict['file_list']) == 0:
            continue
        response_msg = self.msg_dict['file_list'].pop()

        # extract the list from the message
        response_msg = response_msg.get_message()
        files_list = self.extract_list(response_msg)
        return files_list

    def download(self, file_name: str, save_as: str):
        """
        this method allows the user to download a file from the file list.
        :param file_name:
        :return: ture if the file fully downloaded, false if failed
        """

        # create a message that request to download a file from the server
        msg = Message()
        msg.set_request('download')
        msg.set_sender(self.client_name)
        msg.set_message(file_name)

        # send the message to the server
        self.send_msg(msg)
        # listen to the server response
        while len(self.msg_dict['download_response']) == 0:
            continue
        response_msg = self.msg_dict['download_response'].pop()

        if response_msg.get_message() == "ERR":
            # file not exist
            return False

        # establish connection with the server
        server_port, client_port, window_size = str(response_msg.get_message()).split(",")
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_port = int(server_port)
        client_port = int(client_port)
        print("server port : " + str(server_port) + " client port : " + str(client_port))
        window_size = int(window_size)

        # bind with the server
        recv_sock.bind((socket.gethostbyname(socket.gethostname()), client_port))

        expected_seq = 0
        # remove the file if exists
        if os.path.exists(save_as):
            os.remove(save_as)

        file = open(save_as, 'a')
        stopped = False
        last_byte = 0

        while True:

            # listen to the server and convert packets into message objects
            msg_bytes = recv_sock.recv(1024)

            if not stopped:
                last_byte = msg_bytes[-1]
            # check if received a PROCEED message from the server, wait for user reply
            if msg_bytes.decode() == "PROCEED":
                stopped = True
                self.msg_dict['proceed_messages'].append(last_byte)
                while len(self.msg_dict['proceed_messages']) != 0:
                    continue
                send_sock.sendto("Y".encode(), (self.server_address, server_port))
                print("sent YES")
                continue

            msg = Message()
            msg.load(msg_bytes.decode())
            print(msg.to_string())
            if msg.get_message() == "DONE":
                break

            # continue receiving messages
            seq_number = int(msg.get_seq())
            data = msg.get_message()

            # send back an ACK
            res_msg = Message()
            if seq_number == expected_seq:
                res_msg.set_message("ACK")
                res_msg.set_seq(expected_seq)
                send_sock.sendto(res_msg.to_string().encode(), (self.server_address, server_port))
                expected_seq += 1
                file.write(data)
            else:
                res_msg.set_message("ACK")
                if expected_seq == 0:
                    res_msg.set_seq(expected_seq)
                else:
                    res_msg.set_seq(expected_seq - 1)
                send_sock.sendto(res_msg.to_string().encode(), (self.server_address, server_port))

        print("SUCCESS")
        recv_sock.close()
        send_sock.close()
        return True

    def extract_list(self, message: str) -> list:
        """
        this method receive a string of users/files and extract a list from it
        by parsing the string name by name.
        :param message: "<name1><name2><name3>....<nameN>" is the input for extract_list function
        :return: a list of strings -> ["name1","name2",....,"nameN"]
        """
        users_list = message[1:-2].split("><")
        for file in users_list:
            print(file)
            if (file == "'__init__.py'") or (file == "'serverGUI.py'"):
                users_list.remove(file)
        return users_list
