#include <iostream>
int main() {
 
      int battery_percentage = 80;
      double obstacle_distance = 1.5;
      bool left_path = true;
      bool right_path = true ;
      bool emergency_status = true;
 
     if (emergency_status) {
         std::cout<<"EMERGENCY_STOP" <<std::endl;
     }
     else if (battery_percentage <= 20){
         std::cout<<"LOW_BATTERY_STOP" <<std::endl;
     }
     else if (obstacle_distance >= 0.8) {
         std::cout<<"MOVE_FORWARD" <<std::endl;
     }
     else if (left_path) {
         std::cout<<"TURN_LEFT" <<std::endl;
     }
     else if (right_path) {
         std::cout<<"TURN_RIGHT" <<std::endl;
         }
     else {
         std::cout<<"PATH_BLOCKED_STOP" <<std::endl;
     }
     return 0; 
 }

     

