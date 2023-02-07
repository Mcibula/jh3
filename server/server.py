import math
import pickle
import socket
import threading
from typing import Tuple


class ThreadedServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 65432) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

    def listen(self) -> None:
        self.socket.listen()

        while True:
            conn, addr = self.socket.accept()
            conn.settimeout(30)

            print(f'Connected to {addr}')

            threading.Thread(
                target=self.receive,
                args=(conn, addr)
            ).start()

    @staticmethod
    def receive(conn: socket.socket, addr: Tuple[str, int]) -> bool:
        while True:
            try:
                data = conn.recv(1024)

                if data:
                    print(data.decode())

                if data.decode() == 'get_joint_config':
                    deg = math.pi / 180
                    conn.sendall(pickle.dumps([0 * deg, 0 * deg, 0 * deg, 45 * deg, 80 * deg, 0 * deg]))

            except socket.timeout:
                conn.close()
                print(f'Connection to {addr} has been closed')

                return False


if __name__ == '__main__':
    ThreadedServer().listen()
