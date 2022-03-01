import threading
import unittest
import time

from src.server.server import Server
from src.client.client import Client
from src.server.message import Message


class TestServerMethods(unittest.TestCase):

    def test_connected_response(self):
        c1 = Client()
        s = Server()
        server_thread = threading.Thread(target=s.listen2)
        server_thread.start()
        client_name = "test_name"

        # given an ip of a nonexistant server, will the client be able to detect that it cant connect
        c1.login(client_name, "127.0.0.2")
        connection_failed = c1.connected
        # given an ip of an existant server, will the client be able to connect
        c1.login(client_name, "127.0.0.1")
        connection_success = c1.connected

        self.assertFalse(connection_failed)
        self.assertTrue(connection_success)

    def test_disconnected(self):
        c1 = Client()
        s = Server()
        server_thread = threading.Thread(target=s.listen2)
        server_thread.start()
        client_name = "test_name"

        c1.logout()
        disconnect_fail = c1.connected
        c1.login(client_name, "127.0.0.1")
        c1.logout()
        disconnect_success = c1.connected

        self.assertFalse(disconnect_fail)
        self.assertTrue(disconnect_success)

    def test_get_users_list(self):
        c1 = Client()
        s = Server()
        server_thread = threading.Thread(target=s.listen2)
        server_thread.start()
        client_name1 = "test_name1"

        c1.login(client_name1, "127.0.0.1")
        user_list1 = c1.get_users_list()

        c2 = Client()
        client_name2 = "test_name2"
        c2.login(client_name2, "127.0.0.1")

        user_list2 = c2.get_users_list()

        self.assertEqual([client_name1], user_list1)
        self.assertEqual([client_name1, client_name2], user_list2)
        # no need to test with no users on as in that case you cannot call the command anyways.

    def test_get_files_list(self):
        s = Server()
        server_thread = threading.Thread(target=s.listen2)
        server_thread.start()
        c1 = Client()
        client_name1 = "test_name1"

        c1.login(client_name1, "127.0.0.1")
        files_list = c1.get_files_list()

        self.assertEqual(['TestMessageTypes.py'], files_list)

    def test_private_message(self):
        s = Server()
        server_thread = threading.Thread(target=s.listen2)
        server_thread.start()
        c1 = Client()
        c2 = Client()
        client_name1 = "test_name1"
        client_name2 = "test_name2"
        c1.login(client_name1, "127.0.0.1")
        c2.login(client_name2, "127.0.0.1")

        client_thread = threading.Thread(target=c2.listen_msg())
        client_thread.start()
        c1.private_msg("test message", client_name2)


if __name__ == '__main__':
    unittest.main()
