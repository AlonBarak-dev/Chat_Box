import threading

import server
from serverGUI import serverGUI
from src.client.clientGUI import ClientGUI


def server_run():
    s = serverGUI()


def client_run():
    c = ClientGUI()


if __name__ == '__main__':
    # server_thread = threading.Thread(target= server_run())
    client_thread = threading.Thread(target=client_run())
    client_thread.start()
    # server_thread.start()
