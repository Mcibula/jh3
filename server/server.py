import math
import pickle
import socket
import threading
from typing import Tuple


class ThreadedServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 65432) -> None:
        """
        Multithreaded TCP socket server serving multiple clients

        :param host: IP of the server
        :param port: Serving port
        """

        # Initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

    def listen(self) -> None:
        """
        Create a new connection
        """

        self.socket.listen()

        while True:
            # Accept incoming connection and set an inactivity timeout to 30 seconds
            conn, addr = self.socket.accept()
            conn.settimeout(30)

            print(f'Connected to {addr}')

            # Start a new listening thread
            threading.Thread(
                target=self.receive,
                args=(conn, addr)
            ).start()

    @staticmethod
    def receive(conn: socket.socket, addr: Tuple[str, int]) -> bool:
        """
        Receive and/or send data

        :param conn: Open connection socket
        :param addr: Tuple of an IP address and port of a client

        :return: False, if the connection has timed out
        """

        while True:
            try:
                # Receive 1024 B of data
                data = conn.recv(1024)

                # If there is some data
                if data:
                    print(data.decode())

                # If `get_joint_config` request is received
                if data.decode() == 'get_joint_config':
                    # Send back new data
                    deg = math.pi / 180
                    conn.sendall(pickle.dumps([0 * deg, 0 * deg, 0 * deg, 45 * deg, 80 * deg, 0 * deg]))

            except socket.timeout:
                # In case of time out
                # Close the connection
                conn.close()
                print(f'Connection to {addr} has been closed')

                # Terminate this thread
                return False


if __name__ == '__main__':
    ThreadedServer().listen()
