import threading
from clientGUI import ClientGUI


def run_client():
    client = ClientGUI()


if __name__ == '__main__':
    client_thread = threading.Thread(target=run_client())
    client_thread.start()