#include <iostream>
#include <string>
#include "libs/robot_libs.h"

void cout_servos_degrees(Robot* robot) {
    // Gets angles of all joints in the robot's arm
    double* servos_degrees = robot->getRoboticArm()->getServoActualPositionsInDegrees();
    
    std::cout << "Servo angles ";
    for (int i = 0; i < 5; i++) {
        std::cout << servos_degrees[i] << " ";
    }
    std::cout << endl;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        return 1;
    }

    std::string port = argv[1];

    // Robot initialization
    auto *robot = new Robot();
    int fd = robot->initConnection(port);

    RobotMotion robotMotion = RobotMotion();
    robotMotion.initArmPosition(robot, fd);

    // Command is an input from python interface
    std::string command;

    // Coordinates of the arm effector position
    int x = 0, y = 0, z = 0, obj_width = 0;

    // Holds coordinates of the effector in the current position
    cv::Point3i current_effector_position = robotMotion.baseArmPoint;

    // Always listens for an input from STDIN
    while (true) {
        command = "";

        // Char "i" tell python interface what to expect
        // Input
        std::cout << "i ";
        std::cin >> command;

        if (command == "forward"){
            std::cin >> x;
            robotMotion.moveFWD(robot, fd, x);
        }
        else if (command == "backward") {
            std::cin >> x;
            robotMotion.moveBWD(robot, fd, x);
        }
        else if (command == "right") {
            std::cin >> x;
            robotMotion.turnRight(robot, fd, x);
        }
        else if (command == "left") {
            std::cin >> x;
            robotMotion.turnLeft(robot, fd, x);
        }
        else if (command == "moveArm") {
            std::cin >> x >> y >> z;

            // Creates a coordinate triple
            cv::Point3i next_effector_position(x, y, z);

            // Moves the robotic arm and updates the current effector position
            robotMotion.moveArm(current_effector_position, next_effector_position, robot, fd);
            current_effector_position = next_effector_position;
            
            cout_servos_degrees(robot);
        }
        else if (command == "grab") {
            std::cin >> obj_width;
            robotMotion.grip(robot, fd, obj_width);
        }
        else if (command == "release") {
            robotMotion.ungrip(robot, fd);
        }
        else if (command == "loadUp") {
            std::cin >> x >> y >> z >> obj_width;
            
            cv::Point3i target_point(x, y, z);
            cv::Point3i over_target_point(x, y + 20, z);

            robotMotion.moveArm(current_effector_position, over_target_point, robot, fd);
            robotMotion.moveArm(over_target_point, target_point, robot, fd);
            cv::waitKey(500);
            robotMotion.grip(robot, fd, obj_width);
            cv::waitKey(500);
            robotMotion.moveArm(target_point, robotMotion.cargoPoint, robot, fd);
            cv::waitKey(500);
            robotMotion.ungrip(robot, fd);
            cv::waitKey(500);
            robotMotion.moveArm(robotMotion.cargoPoint, robotMotion.baseArmPoint, robot, fd);
            
            current_effector_position = robotMotion.baseArmPoint;
            cout_servos_degrees(robot);
        }
        else if (command == "try") {
            std::cin >> x >> y >> z;
            cv::Point3i target_point(x, y, z);
            
            std::cout << "Result ";
            
            if (robotMotion.getDistance(current_effector_position, target_point) < 10) {
                std::cout << 2 << endl;
            }
            else {
                vector<cv::Point3i> path = robotMotion.calculatePath(current_effector_position, target_point);
                bool point_is_good = true;
                
                for (int i = 1; i < path.size(); i++) {
                    int* prevArm = robot->getServoPositions();
                    int* nextArm = robot->getServoPositions();

                    int q2Degree = 30;
                    bool inverseResult = false;
                    while (!inverseResult && q2Degree <= 125) {
                        inverseResult = robot->getRoboticArm()->find_solution_and_do_InverseKinematics(path[i].x, path[i].z, path[i].y, q2Degree);
                        q2Degree++;
                        nextArm = robot->getServoPositions();
                    }

                    if (!inverseResult) {
                        point_is_good = false;
                        break;
                    }
                }
                
                if (point_is_good) {
                    
                    std::cout << 1 << endl;
                }
                else {
                    
                    std::cout << 0 << endl;
                }
            }
        }
    }

    return 0;
}
