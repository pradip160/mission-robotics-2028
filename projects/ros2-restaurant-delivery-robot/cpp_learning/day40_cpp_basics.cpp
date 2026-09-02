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

struct RobotConfig
{
    double safe_front_distance;
    int low_battery_threshold;
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



constexpr double SAFE_FRONT_DISTANCE = 1.5;

bool is_front_path_clear(double obstacle_distance)
{
    return obstacle_distance > SAFE_FRONT_DISTANCE;
}

constexpr int LOW_BATTERY_THRESHOLD = 20; 
bool is_battery_safe(
    int battery_percentage,
    int low_battery_threshold
)
{ 
    return battery_percentage > low_battery_threshold;
}


RobotCommand decide_movement(
    const RobotState& robot,
    const RobotConfig& config 
)
{
    if (robot.emergency_status)
        return RobotCommand::EMERGENCY_STOP;

    if (!is_battery_safe(
        robot.battery_percentage,
        config.low_battery_threshold
    ))
        return RobotCommand::LOW_BATTERY_STOP;

    if (is_front_path_clear(robot.obstacle_distance))
        return RobotCommand::MOVE_FORWARD;

    if (robot.left_path)
        return RobotCommand::TURN_LEFT;

    if (robot.right_path)
        return RobotCommand::TURN_RIGHT;

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
      robot.obstacle_distance = 1.0; 
      robot.left_path = true;
      robot.right_path = true ;
      robot.emergency_status = false;

      RobotConfig config;
 
      config.safe_front_distance = 1.5;
      config.low_battery_threshold = 20;


      RobotCommand movement_command = decide_movement(robot, config);
      print_robot_command(movement_command);
      
      return 0;
 
} 
     


     

 


