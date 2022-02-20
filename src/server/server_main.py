import threading
from serverGUI import serverGUI

def server_run():
    s = serverGUI()


if __name__ == '__main__':
    server_thread = threading.Thread(target=server_run())
    server_thread.start()
