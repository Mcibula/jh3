#include <iostream>
#include <string>
#include "libs/robot_libs.h"

using namespace std;

static string port;

int main() {
    Robot *robot = new Robot();
    int fd = robot->initConnection(port);

    RobotMotion robotMotion = RobotMotion();
    robotMotion.initArmPosition(robot, fd);

    string line;
    string buffer;
    int x, y, z;
    cv::Point3i current_arm_position = robotMotion.baseArmPoint;

    while (true) {
        line = "";
        getline(cin, line);

        if (line == "forward") {
            robotMotion.moveFWD(robot, fd);
        }
        else if (line == "backward") {
            robotMotion.moveBWD(robot, fd);
        }
        else if (line == "right") {
            robotMotion.turnRight(robot, fd);
        }
        else if (line == "left") {
            robotMotion.turnRight(robot, fd);
        }
        else if (line.rfind("moveArm") == 0) {
            istringstream(line) >> buffer >> x >> y >> z;

            cv::Point3i next_position(x, y, z);
            robotMotion.moveArm(current_arm_position, next_position, robot, fd);
            current_arm_position = next_position;
        }
        else if (line == "grab") {
            robotMotion.grip(robot, fd, 10);
        }
        else if (line == "ungrab") {
            robotMotion.ungrip(robot, fd);
        }
    }
    return 0;
}