#include <iostream> 
int main() {

    int battery = 85;
    double obstacle_distance = 1.5;
    bool robot_ready = true; 


    if (battery > 20 && obstacle_distance > 0.8) {
        std::cout<< "MOVE_FORWARD" << std::endl;
    }
    else {
        std::cout<< "STOP" << std::endl;
    }

    std::cout<< "Restaurant Robot online" << std::endl;
    std::cout<< "Battery: " << battery << "%" << std::endl;
    std::cout<< "obstacle: " << obstacle_distance << std::endl;
    std::cout<< "robot_ready: "<< robot_ready << std::endl;
    return 0;
}
