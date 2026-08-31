#include <iostream>
#include <string>

struct RobotState 
{
    int battery_percentage;
    double obstacle_distance;
    bool left_path;
    bool right_path;
    bool emergency_status;
};

enum class RobotCommand 
{
    EMERGENCY_STOP,
    LOW_BATTERY_STOP,
    MOVE_FORWARD,
    TURN_LEFT,
    TURN_RIGHT,
    PATH_BLOCKED_STOP
};


bool is_battery_safe(int battery_percentage)
{
    if (battery_percentage > 20) {
       return true;
    }
    else {
        return false;
    }
}

bool is_emergency(bool emergency_status)
{
    return emergency_status;
}


RobotCommand decide_movement(const RobotState& robot)
{
    if (robot.emergency_status)
        return RobotCommand::EMERGENCY_STOP;

    else if (robot.battery_percentage <= 20)
        return RobotCommand::LOW_BATTERY_STOP;

    else if (robot.obstacle_distance > 1.5)
        return RobotCommand::MOVE_FORWARD;

    else if (robot.left_path)
        return RobotCommand::TURN_LEFT;

    else if (robot.right_path)
        return RobotCommand::TURN_RIGHT;
 
    else 
        return RobotCommand::PATH_BLOCKED_STOP;
}


void print_robot_command(RobotCommand command)
{
switch (command)
    {
    case RobotCommand::EMERGENCY_STOP:
        std::cout << "EMERGENCY_STOP" << std::endl;
        break;
    case RobotCommand::LOW_BATTERY_STOP:
        std::cout <<"LOW_BATTERY_STOP" << std::endl;
        break;

    case RobotCommand::MOVE_FORWARD:
        std::cout <<"MOVE_FORWARD" << std::endl;
        break;
 
    case RobotCommand::TURN_LEFT:
        std::cout <<"TURN_LEFT" << std::endl;
        break;

    case RobotCommand::TURN_RIGHT:
        std::cout << "TURN_RIGHT" << std::endl;
        break;

    case RobotCommand::PATH_BLOCKED_STOP:
        std::cout << "PATH_BLOCKED_STOP" << std::endl;
        break;
 
    }
}

int main() {

      RobotState robot;

      robot.battery_percentage = 30;
      robot.obstacle_distance = 1.5; 
      robot.left_path = true;
      robot.right_path = true ;
      robot.emergency_status = false;


      RobotCommand movement_command = decide_movement(robot);
      print_robot_command(movement_command);
      
      return 0;
 
} 
     


     

 


