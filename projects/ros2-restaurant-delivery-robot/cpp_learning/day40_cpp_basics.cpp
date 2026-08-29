#include <iostream>
#include <string>

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

std::string decide_movement (double obstacle_distance, bool left_path, bool right_path)
{
    if (obstacle_distance >= 0.8) {
        return "MOVE_FORWARD";
    }
    else if (left_path) {
        return "TURN_LEFT";
    } 
    else if (right_path) {
        return "TURN_RIGHT";
    }
    else {
        return "PATH_BLOCKED_STOP";
    }
}

void print_robot_command(std::string command)
{
    std::cout << command << std::end;
}


int main() {
 
      int battery_percentage = 30;
      double obstacle_distance = 1.5;
      bool left_path = true;
      bool right_path = true ;
      bool emergency_status = false;
 
     if (is_emergency(emergency_status)) {
         std::cout<<"EMERGENCY_STOP" <<std::endl;
     }
     else if (!is_battery_safe(battery_percentage)) {
         std::cout<<"LOW_BATTERY_STOP" <<std::endl;
     }
     else {
         std::string movement_command = decide_movement(obstacle_distance, left_path, right_path);
         print_robot_command(movement_command);
     } 
     return 0; 
 }

     

 
