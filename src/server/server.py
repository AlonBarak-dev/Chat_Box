import _thread
import os
import socket
import threading
import time

from message import Message
from Timer import Timer


class Server:

    def __init__(self, address=None):
        # a dict to hold all of the connected clients
        # {"client_name": client_sock}
        self.clients = {}

        # list of all files located in the server
        self.file_list = os.listdir()
        for file in self.file_list:
            if 'py' in file:
                self.file_list.remove(file)

        # Create a STREAM socket
        self.receive_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # create a DGRAM socket
        self.receive_socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.receive_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the receive socket
        self.server_port = 50000
        self.server_udp_port = 50001
        # initialize the IP address of the server
        self.ip = address

        self.receive_socket.bind((self.ip, self.server_port))
        self.receive_socket_udp.bind((self.ip, self.server_udp_port))

        self.receive_socket.listen(15)
        self.new_client_id = 1
        # a dict for ports
        # {client_name: (server_port, client_port)}
        self.port_dict = {}
        # a list of available ports
        self.ports = [i for i in range(55000, 55020)]

        # selective repeat
        self.lock = _thread.allocate_lock()
        self.base = 0
        self.timer = Timer(0.5)
        self.stop = True
        self.proceed = False

    def send_response(self, msg: Message):
        """
        this method receive a message that the server prepared to a client and
        responsible for sending the message to the desired client
        :param msg: a message object that contains all the information og the packet
        """
        print(msg.to_string())
        # get the client info
        time.sleep(0.1)
        dest_client = msg.get_receiver()
        if dest_client == "Server":
            return
        # convert the message object to a string
        msg_bytes = msg.to_string().encode()
        # send the message to the desired client
        self.clients[str(dest_client)].send(msg_bytes)

    def run_client(self, sock, address, client_id):
        """
        this method listening to messages from all clients and call the specific function that can handle the
        client request. for example, if the request is a connect type then this method will call
        to the connection response function.
        """

        while True:
            # listen to a packet from the clients
            msg = sock.recv(65536)

            # convert the bytes to string
            msg = msg.decode()

            # convert from string to a message object
            msg_obj = Message()
            msg_obj.load(msg)

            # investigate the message request
            msg_type = str(msg_obj.get_request())

            # check the message type
            if msg_type == 'connect':
                self.connected_response(msg_obj, client_id)
            elif msg_type == 'disconnect':
                self.disconnected(msg_obj)
            elif msg_type == 'get_user_list':
                self.users_list(msg_obj)
            elif msg_type == 'get_file':
                self.files_list(msg_obj)
            elif msg_type == 'message_request':
                self.msg_sent(msg_obj)
            elif msg_type == 'download':
                # start another thread for download communication so other platforms will still work at the same time
                thread = threading.Thread(target=self.downloaded, args=(msg_obj, address[0],))
                thread.start()

    def listen2(self):
        """
        this method is responsible for accepting connect requests from clients
        """
        while True:
            # accept a connection from a client
            sock, address = self.receive_socket.accept()
            print(address)
            # temporary key for the socket
            self.clients[str(self.new_client_id)] = sock

            # create a new thread for the new client and start it
            client_thread = threading.Thread(target=self.run_client, args=(sock, address, str(self.new_client_id),))
            self.new_client_id += 1
            client_thread.start()

    def connected_response(self, message: Message, client_id):
        """
        this method responsible to connect the client to the server
        base on the request
        :param message: a message object that contain all the information about the request
        :return: true message if login successfully, else return false message
        """

        # create a response message to be send to the client
        res_msg = Message()

        # initialize the client fields
        flag = True
        client_name = str(message.get_sender())
        if client_name in self.clients.keys():
            flag = False
        # set the name of the client as the key to its socket
        data = self.clients[client_id]
        del self.clients[client_id]
        self.clients['' + client_name] = data
        # edit the response message
        res_msg.set_response('connect_response')
        res_msg.set_sender('server:' + self.ip)
        res_msg.set_receiver(client_name)
        res_msg.set_message(flag)

        # send the response message to the client
        self.send_response(res_msg)

        # send a broadcast message that a new client has joined the chat group
        brd_msg = Message()
        brd_msg.set_receiver("all")
        brd_msg.set_message("New User joined out Chat Box! Say hello to " + client_name + " :)")
        brd_msg.set_sender("Server")
        self.msg_sent(brd_msg)

    def disconnected(self, message: Message):
        """
        this method handle a disconnect request.
        it removes the client from the users list and clode the
        communication between the serverand the client.
        :param message: a Message object that contains all the info about
        the request.
        :return: true message if login successfully, else return false message
        """

        # create a message to be sent to the client
        res_msg = Message()
        res_msg.set_response('disconnect_response')
        res_msg.set_receiver(message.get_sender())
        res_msg.set_sender('server:' + self.ip)
        # delete the client if exist
        if message.get_sender() in self.clients:
            res_msg.set_message(True)
        else:
            res_msg.set_message(False)
        # send the message to the client
        self.send_response(res_msg)
        del self.clients[message.get_sender()]

    def msg_received(self, message: Message, user_name: str):
        """
        this method is responsible on sending a message to a specific user.
        :param message: a message object that contains the content wanted to be delivered
        :param user_name: the client which will get the message
        :return: true if sent, false if not
        """

        # check if the desired user is a client
        if user_name not in self.clients:
            return False

        # create a message that will be delivered to the chosen client
        res_msg = Message()
        res_msg.set_response('message_received')
        res_msg.set_message(message.get_message())
        res_msg.set_sender(message.get_sender())
        res_msg.set_receiver(user_name)
        # send the message to the client
        self.send_response(res_msg)

        return True

    def msg_sent(self, message: Message):
        """
        this method is called once a client want to send a private/public message.
        if private, the method will call the self.message_received method on the specific
        client.
        if all, the method will call the self.message_received method on every single client
        that connected to the server at the moment
        :param message: the message that contains all the infomation about the
        message request
        :return: A true message if success. False otherwise.
        """

        # create a message to be sent once the server finish the process
        res_msg = Message()
        sent_flag = True

        # check if the message is private or broadcast
        message_dest = message.get_receiver()
        if message_dest == 'all':
            # send broadcast
            # loop over the server's clients and send the message for each one of them
            for client in self.clients.keys():
                sent_flag = self.msg_received(message, client)
        else:
            # send the message to the specific client
            sent_flag = self.msg_received(message, message_dest)

        # edit the message base on the data
        res_msg.set_message(sent_flag)
        res_msg.set_response('message_response')
        res_msg.set_sender('server:' + self.ip)
        res_msg.set_receiver(message.get_sender())
        # send the response message back to the sender
        self.send_response(res_msg)

    def users_list(self, message: Message):
        """
        this method return a response message that contains a list with all the server's client's names
        ['name1','name2',....'nameN']
        :param message: a message object containing all the info about the
        client request
        :return: a message with list of strings
        """

        # create a response message to be sent to the client
        res_msg = Message()

        # create a list with all user's names
        users_list = []
        for name in self.clients.keys():
            users_list.append(name)

        # edit the response message base on the data
        res_msg.set_message(users_list)
        res_msg.set_sender('server:' + self.ip)
        res_msg.set_receiver(message.get_sender())
        res_msg.set_response('user_list')

        # send the message to the client
        self.send_response(res_msg)

    def files_list(self, message: Message):
        """
        this method return a list of all files available to download which located at the server.
        :param message: a message object contains all the info about the clients request
        :return: a list of string ['ffile1',file2',....'fileN']
        """

        # create a response message to be send to the client
        res_msg = Message()

        # edit the response message base on the data
        res_msg.set_message(self.file_list)
        res_msg.set_response('file_list')
        res_msg.set_receiver(message.get_sender())
        res_msg.set_sender('server:' + self.ip)

        # send the response message to the client
        self.send_response(res_msg)

    def downloaded(self, message: Message, client_address: str):
        """
        this method transfer a stream of bytes that represent a file in the server to the client.
        :param message: a message object tha contains all the info about the client request
        :return: a message that contains a file as a stream of bytes.
                return 'ERR' in case the file does not exist in the server
        """

        # create a response message to be send to the client
        res_msg = Message()
        flag_return = False
        self.stop = False
        window_size = 0
        server_port = 0
        client_port = 0
        packets = {}
        seq = 0
        file = None
        # if the file doesnt exist in the server return an error message
        if not os.path.exists(str(message.get_message())):
            res_msg.set_message("ERR")
            flag_return = True
        else:
            file = open(message.get_message(), 'rb')
            # add all packets to the buffer
            while True:
                data = file.read(100).decode()
                if not data:
                    break
                packets[str(seq)] = data
                seq += 1
            # define window size
            window_size = int(seq / 4) + 1
            # generate ports numbers
            server_port = int(self.ports[0])
            client_port = int(self.ports[1])
            del self.ports[0]
            del self.ports[1]
            self.port_dict[message.get_sender()] = (server_port, client_port)
            # set the message content as the chosen ports
            # "server_port,client_port,number_of_packet,window_size"
            res_msg.set_message(str(server_port) + "," + str(client_port) + "," + str(window_size))

        # edit the message base on the data
        res_msg.set_response('download_response')
        res_msg.set_sender('server:' + self.ip)
        res_msg.set_receiver(message.get_sender())

        # send the message to the client
        self.send_response(res_msg)
        # if the file doesnt exist, return
        if flag_return:
            return

        # establish a UDP connection with the client
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind with the receive socket
        recv_sock.bind((self.ip, server_port))
        print("server port : " + str(server_port) + " client port : " + str(client_port))

        number_of_packets_needed = seq
        latest_packet_sent = 0
        self.base = 0
        # listen to ACKs from the client
        recv_sock.settimeout(3)
        _thread.start_new_thread(self.receive_udp, (recv_sock,))

        seq = -1
        msg = Message()
        stop = True
        break_flag = False

        # run over the entire file
        while self.base < number_of_packets_needed:
            self.lock.acquire()
            while latest_packet_sent < self.base + window_size:
                # trying to stop the process so the client can confirm
                if (latest_packet_sent > number_of_packets_needed/4) and (latest_packet_sent < number_of_packets_needed/2) \
                        and stop:
                    send_sock.sendto("PROCEED".encode(), (client_address, client_port))
                    print("PROCEED?")
                    self.lock.release()
                    while not self.proceed:
                        continue
                    self.lock.acquire()

                # continue sending packets
                msg.set_seq(latest_packet_sent)
                msg.set_message(packets[str(latest_packet_sent)])
                print(msg.to_string())
                send_sock.sendto(msg.to_string().encode(), (client_address, client_port))
                latest_packet_sent += 1

            # start the RTT timer
            if not self.timer.running():
                self.timer.start()

            # wait until the end of the RTT or a ACK is received
            while self.timer.running() and not self.timer.timeout():
                self.lock.release()
                time.sleep(0.05)
                self.lock.acquire()

            # check for timeout
            if self.timer.timeout():
                self.timer.stop()
                latest_packet_sent = self.base
            else:
                window_size = min(window_size, number_of_packets_needed - self.base)

            self.lock.release()

        msg.set_message("DONE")
        seq += 1
        msg.set_seq(seq)
        send_sock.sendto(msg.to_string().encode(), (client_address, client_port))
        print(msg.to_string())

        self.ports.append(server_port)
        self.ports.append(client_port)
        self.stop = True
        self.proceed = False
        send_sock.close()

    def receive_udp(self, recv_sock: socket):
        """
        this method receives ACKS from the client
        :param recv_sock: a UDP socket
        :return:
        """
        while True:
            try:
                message = recv_sock.recv(1024)
            except socket.timeout:
                if self.stop:
                    break
                else:
                    continue
            if message.decode() == "Y":
                print("YES")
                self.lock.acquire()
                self.proceed = True
                self.lock.release()
                continue
            message = message.decode()
            msg = Message()
            msg.load(message)
            print(msg.to_string())
            ack = int(msg.get_seq())
            if ack >= self.base:
                self.lock.acquire()
                self.base = ack + 1
                self.timer.stop()
                self.lock.release()
        recv_sock.close()