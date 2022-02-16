from pip._internal.utils.misc import enum


class Message:

    def __init__(self, message=None):

        self.key_to_prefix = {
            "message": "m:",
            "sender": "s:",
            "recipient": "r:",
            "request": "q:",
            "response": "p:"
        }
        self.prefix_to_key = {
            "m:": "message",
            "s:": "sender",
            "r:": "recipient",
            "q:": "request",
            "p:": "response"
        }

        self.request_types = enum('connect', 'disconnect', 'get_user_list', 'get_file',
                                  'message_request', 'download')

        self.response_types = enum('connect_response', 'disconnect_response', 'user_list', 'file_list',
                                   'message_response', 'download_response')

        self.info = {
            "message": None,  # content of the actual message
            "sender": None,  # the name of the sender
            "recipient": None,  # the name of the recipient / "all" for broadcast
            "request": None,  # connect/disconnect/get_user_list/get_file/port_request
            "response": None
        }

        if message is not None:
            self.load(message)

    # gets a message as a string and loads the data into the fields of the object
    def load(self, message):
        fields = message[1:-2].split("><")
        for field in fields:
            self.info[self.prefix_to_key[field[0: 2]]] = field[2, -1]

    # makes a string out of the message
    def to_string(self):
        string_to_send = ""
        for key in self.info:
            if self.info[key] is None:
                continue
            string_to_send += "<" + self.key_to_prefix[key] + str(self.info[key]) + ">"
        return string_to_send

    def set_sender(self, sender):
        self.info["sender"] = sender
        return True

    def set_message(self, message):
        self.info["message"] = message
        return True

    def set_receiver(self, receiver):
        self.info["recipient"] = receiver
        return True

    def set_request(self, request):
        if request is None or request in self.request_types:
            self.info["request"] = request
            return True
        return False

    def set_response(self, response):
        if response is None or response in self.response_types:
            self.info["response"] = response
            return True
        return False

    def get_sender(self):
        return self.info["sender"]

    def get_message(self):
        return self.info["sender"]

    def get_receiver(self):
        return self.info["sender"]

    def get_request(self):
        return self.request_types[self.info["request"]]

    def get_response(self):
        return self.response_types[self.info["response"]]
