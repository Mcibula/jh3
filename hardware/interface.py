from typing import List

import pexpect


class Interface:
    def __init__(self, port: str) -> None:
        """
        Interface communicates with the wrapper of a robot

        :param port: Communication port with the main circuit
        """

        self.wrapper = pexpect.spawn(f'./hardware/wrapper {port}')

    def send_command(self, command: str) -> None:
        """
        Sends commands to the wrapper

        :param command: Command to send
        """

        self.wrapper.expect('i ')
        self.wrapper.sendline(command)

    def forward(self, time: int = 130) -> None:
        """
        Robot goes forwards for a time from input
        
        :param time: Time to send
        """

        self.send_command(f'forward {abs(time)}')

    def backward(self, time: int = 130) -> None:
        """
        Robot goes backwards for a time from input
        
        :param time: Time to send
        """

        self.send_command(f'backward {abs(time)}')

    def turn_right(self, time: int = 260) -> None:
        """
        Robot turns right for a time from input
        
        :param time: Time to send
        """

        self.send_command(f'right {abs(time)}')

    def turn_left(self, time: int = 260) -> None:
        """
        Robot turns left for a time from input
        
        :param time: Time to send
        """

        self.send_command(f'left {abs(time)}')

    def move_arm(self, x: int, y: int, z: int) -> List[float]:
        """
        Robot moves arm, so that the effector is on coordinates x, y, z

        :param x: Effector X-axis coordinate
        :param y: Effector Y-axis coordinate
        :param z: Effector Z-axis coordinate
        :return: List of floats - angles of each joint in robotic arm
        after it finished all movements
        """

        self.send_command(f'moveArm {x} {y} {z}')
        self.wrapper.expect('Servo angles')
        output = self.wrapper.readline().decode().split()

        return list(map(float, output))

    def grab(self, width: int = 15) -> None:
        """
        Robot puts clamps of the effector to width from input
        
        :param width: Width to send
        """
        
        self.send_command(f'grab {abs(width) % 30}')

    def release(self) -> None:
        """
        Robot opens clamps of effector to default width of ~30mm
        """

        self.send_command('release')

    def load_up(self, x: int, y: int, z: int, obj_width: int) -> List[float]:
        """
        Robot picks up an object with middle point coordinates and width
        from input. Then the robot puts the object to the cargo box and
        resets arm to default position
        
        :param x: Object middle point X-axis coordinate
        :param y: Object middle point Y-axis coordinate
        :param z: Object middle point Z-axis coordinate
        :param obj_width: Width of the object
        :return: List of floats - angles of each joint in robotic arm
        after it finished all movements
        """
        
        self.send_command(f'loadUp {x} {y} {z} {obj_width}')
        self.wrapper.expect('Servo angles ')
        output = self.wrapper.readline().decode().split()

        return list(map(float, output))

    def try_point(self, x: int, y: int, z: int) -> int:
        """
        Robot calculates if a point with coordinates from input is a valid
        target point for the effector
        
        :param x: Target point X-axis coordinate
        :param y: Target point Y-axis coordinate
        :param z: Target point Z-axis coordinate
        :return: 0 - point is not valid
                 1 - point is valid
                 2 - point is too close to the current effector position
        """
        
        self.send_command(f'try {x} {y} {z}')
        self.wrapper.expect('Result ')
        
        output = self.wrapper.readline().decode().strip()
        
        return int(output)
