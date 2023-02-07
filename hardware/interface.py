from typing import List

import pexpect


class Interface:
    def __init__(self) -> None:
        """
        Interface communicates with the wrapper of a robot
        """

        self.wrapper = pexpect.spawn('./wrapper.exe')

    def send_command(self, command: str) -> None:
        """
        Sends commands to the wrapper

        :param command: Command to send
        """

        self.wrapper.expect('i ')
        self.wrapper.sendline(command)

    def forward(self) -> None:
        """
        Robot goes forwards a bit
        """

        self.send_command('forward')

    def backward(self) -> None:
        """
        Robot goes backwards a bit
        """

        self.send_command('backward')

    def turn_right(self) -> None:
        """
        Robot turns right a bit
        """

        self.send_command('right')

    def turn_left(self) -> None:
        """
        Robot turns left a bit
        """

        self.send_command('left')

    def move_arm(self, x: int, y: int, z: int) -> List[float]:
        """
        Robot moves arm, so that the effector is on coordinates x, y, z

        :param x: Effector X-axis coordinate
        :param y: Effector Y-axis coordinate
        :param z: Effector Z-axis coordinate
        :return: List of floats - angles of each joint in robotic arm
        """

        self.send_command(f'moveArm {x} {y} {z}')
        self.wrapper.expect('o ')
        output = self.wrapper.readline().decode().split()

        return list(map(float, output))

    def grab(self) -> None:
        """
        Robot closes clamps of the effector to width of ~10 mm
        """

        self.send_command('grab')

    def release(self) -> None:
        """
        Robot opens clamps of effector to default width of ~30mm
        """

        self.send_command('release')
