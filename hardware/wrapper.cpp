#include <iostream>
#include <string>
#include "libs/robot_libs.h"

std::string port;

int main() {
    // Robot initialization
    auto *robot = new Robot();
    int fd = robot->initConnection(port);

    RobotMotion robotMotion = RobotMotion();
    robotMotion.initArmPosition(robot, fd);

    // Command is an input from python interface
    std::string command;

    // Coordinates of the arm effector position
    int x = 0, y = 0, z = 0;

    // Holds coordinates of the effector in the current position
    cv::Point3i current_effector_position = robotMotion.baseArmPoint;

    // Always listens for an input from STDIN
    while (true) {
        command = "";

        // Chars "i" / "o" tell python interface what to expect
        // Input
        std::cout << "i ";
        std::cin >> command;

        // Output
        std::cout << "o ";

        if (command == "forward") {
            robotMotion.moveFWD(robot, fd);
        }
        else if (command == "backward") {
            robotMotion.moveBWD(robot, fd);
        }
        else if (command == "right") {
            robotMotion.turnRight(robot, fd);
        }
        else if (command == "left") {
            robotMotion.turnLeft(robot, fd);
        }
        else if (command == "moveArm") {
            std::cin >> x >> y >> z;

            // Creates a coordinate triple
            cv::Point3i next_effector_position(x, y, z);

            // Moves the robotic arm and updates the current effector position
            robotMotion.moveArm(current_effector_position, next_effector_position, robot, fd);
            current_effector_position = next_effector_position;

            // Gets angles of all joints in the robot's arm
            double* servos = robot->getRoboticArm()->getServoActualPositionsInDegrees();

            // Puts the angles to one string separated by spaces
            std::string servo_angles;
            for (int i = 0; i < 5; ++i) {
                servo_angles += to_string(servos[i]) + " ";
            }
            std::cout << servo_angles;
        }
        else if (command == "grab") {
            robotMotion.grip(robot, fd, 10);
        }
        else if (command == "release") {
            robotMotion.ungrip(robot, fd);
        }
    }

    return 0;
}