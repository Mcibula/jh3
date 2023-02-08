import pickle
import socket
from typing import Tuple, List


class Connection:
    def __init__(self, host: str = '127.0.0.1', port: int = 65432) -> None:
        """
        Class managing a socket connection

        :param host: IP address of the server
        :param port: Port of the server
        """

        self.host = host
        self.port = port

        # Connect to the server
        self._connect()

    def __del__(self) -> None:
        """
        Shutdown and close the connection on a destruction
        """

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def _connect(self) -> None:
        """
        Create a new connection with the server
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def _send(self, data: bytes) -> None:
        """
        Send data

        :param data: Data to send
        """

        try:
            # Send all data through the connection
            self.socket.sendall(data)
        except BrokenPipeError:
            # If the connection is not alive anymore
            # Create a new one and repeat
            self._connect()
            self.socket.sendall(data)

    def move_fwd(self) -> None:
        self._send(b'base_fwd')
        print('Move FWD')

    def move_bwd(self) -> None:
        self._send(b'base_bwd')
        print('Move BWD')

    def move_left(self) -> None:
        self._send(b'base_left')
        print('Move LEFT')

    def move_right(self) -> None:
        self._send(b'base_right')
        print('Move RIGHT')

    def send_coords(self, coords: Tuple[int, int, int]) -> None:
        x, y, z = coords
        self._send(f'move_arm {x} {y} {z}'.encode())
        print(coords)

    def grip(self) -> None:
        self._send(b'effector_grip')
        print('Grab')

    def release(self) -> None:
        self._send(b'effector_release')
        print('Release')

    def get_joint_config(self) -> List[float]:
        self._send(b'get_joint_config')
        q = []

        try:
            data = self.socket.recv(1024)
            q = pickle.loads(data)
        except EOFError:
            pass

        print(q)

        return q


if __name__ == '__main__':
    conn = Connection()
    conn.move_fwd()
