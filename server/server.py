import math
import pickle
import socket
import threading
from typing import Tuple

from hardware.interface import Interface


class ThreadedServer:
    def __init__(
            self,
            host: str = '127.0.0.1',
            port: int = 65432,
            hw_port: str = '/dev/ttyUSB0'
    ) -> None:
        """
        Multithreaded TCP socket server serving multiple clients

        :param host: IP of the server
        :param port: Serving port
        :param hw_port: Port to the serial converter of the robot
        """

        print('Starting server...')

        # Initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

        # Connect to the robot
        print('Initializing hardware interface...')
        self.hardware = Interface(hw_port)

        # Function calls without parameters
        self.calls = {
            'base_fwd': self.hardware.forward,
            'base_bwd': self.hardware.backward,
            'base_left': self.hardware.turn_left,
            'base_right': self.hardware.turn_right,
            'effector_grip': self.hardware.grab,
            'effector_release': self.hardware.release
        }

        # Default joint configuration
        deg = math.pi / 180
        self.joint_config = [0 * deg, 45 * deg, -45 * deg, -45 * deg]

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

    def receive(self, conn: socket.socket, addr: Tuple[str, int]) -> bool:
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
                    print(f'Received "{data.decode()}"')

                    # Decode received command
                    cmd = data.decode().split()
                    func = cmd[0]

                    if func == 'move_arm':
                        # If `move_arm` request is received
                        # Extract coordinates and execute while receiving a new joint config
                        x, y, z = map(int, cmd[1:])

                        # Check if coordinates are valid
                        if self.hardware.try_point(x, y, z) == 1:
                            j_config = self.hardware.move_arm(x, y, z)[1:][::-1]
                            j_config[2] *= (-1)
                            j_config[3] *= (-1)
                            self.joint_config = j_config
                    
                    elif func == 'load_up':
                        # If `load_up` request is received
                        # Extract coordinates and execute while receiving a new joint config
                        x, y, z = map(int, cmd[1:])

                        # Check if coordinates are valid
                        if self.hardware.try_point(x, y, z) == 1:
                            j_config = self.hardware.load_up(x, y, z)[1:][::-1]
                            j_config[2] *= (-1)
                            j_config[3] *= (-1)
                            self.joint_config = j_config

                    elif func == 'get_joint_config':
                        # If `get_joint_config` request is received
                        # Send back a new joint config
                        conn.sendall(pickle.dumps(self.joint_config))

                    elif func in self.calls:
                        # Execute without parameters
                        self.calls[func]()

            except socket.timeout:
                # In case of time out
                # Close the connection
                conn.close()
                print(f'Connection to {addr} has been closed')

                # Terminate this thread
                return False


if __name__ == '__main__':
    # Start the server
    ThreadedServer(host='192.168.241.87').listen()
