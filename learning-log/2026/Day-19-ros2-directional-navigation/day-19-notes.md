# Day 19: ROS2 Directional Navigation

## Learning Evidence
- YouTube video: [https://youtu.be/vCRvxUxCWFE]
- Main navigation file: `projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status/navigation_obstacle_subscriber.py`
- Motor control file: `projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status/motor_control_subscriber.py`
- Topic: Directional awarness, sensor freshness, and safe turning decisions

## Goal 
My goal was to help my robot understand its surrounding and become able to turn right snf 
left insted only moving straight. I wanted to see the robot make navigayion decisions on its own, and today it successfully chose when to turn  right, turn left, move forward, or stop. I also added sensor freshness checks using timer so the robot always acts only on recent and valid sensor messages. 

## Theory 
A robot needs to move smoothly and safely in human enviroment to work efficiently. It must understand whether the front, left, and right directions are safe before choosing a movement command. Without the timer and sensor freshness checks, the robot would not know when each message was published and could act on old information from  the past. This could make the robot move or turn toward an obstacle that appeared after the last sensor message. 

## Implementation

I added a sensor timeout and prepared separate left and right states. I also stored the latest message time for each direction and used freshness variables to record whether the information was still valid. Then I created the `receive_left()` and `receive_right()` callbacks and connected them to the `/left_status` and `/right_status` topics. I expanded `check_sensor_freshness()` so it calculates whether the left and right messages are fresh or stale. Finally, I updated the navigation logic so the robot can choose `TURN_LEFT`, `TURN_RIGHT`, `MOVE_FORWARD`, or `STOP` depending on the front and side information.

## Testing and Reasults

I tested the navigation system with different simulated ROS2 sensor messages. 

First I ran the navigation node wihtout publishing any senosr data. the camera, LiDAR, front, left and right states were unknown, so robot correctly publishes `STOP`.

Then I published `PATH_CLEAR` only from the camera. Because the LiDAR data was still missing, the front state remained `UNKNOWN`,and the robot continued publishing `STOP`.

After that, I published `PATH_CLEAR` from both the camera and LiDAR. The front state became `PATH_CLEAR`, and the robot correctly published `MOVE_FORWARD`.

Next, I changed the LiDAR message to `OBSTACLE_DETECTED` while the camera still reportes `PATH_CLEAR`. the robot trusted the danger report, changed the front state to `OBSTACLE_DETECTED`, and published `STOP` because no safe sidw direction was available. 

I then published `PATH_CLEAR` ON `/left_status`. Because the frint was blcked and the left information was fresh and clear, the robot published `TURN_LEFT`.

I stopped the left-side publisher and waited longer than the three-second timeout. The stored left state still contained `PATH_CLEAR`, BUT `left_fresh` becane false, so the robot correctly changed its command back to stop. 

After that, I published `PATH_CLEAR` on `/right_status`. Because the left data was stale and the right data was fresh and clear, the robot published `TURN_RIGHT`. 

I also ran the motor-control subscriber and confirmed theat ur received `TURN_RIGHT` through `/motor_command`. The motor node logged that the right wheel should slow down while the left wheel moves faster.

Finally, I stopped the right-side publisher and waited longer than three seconds. The right messages became stale, so the navigation node published `STOP`, and the motor-contorl nodelogged that both wheels stopped safely.


## Inspection 

The ROS2 logs showed that the navigatio node was correctly separating sensor sources from physical directions. 

The camera and LiDAR states were combined into one `front_state`. The left and right states were handled sepatately and were trusted only when their messages were fresh. 

The logs also showed that safety conditions were checked before movement conditions. Missing or stale front information ptoduce `STOP`.

When the front was blocked, the robot checked the left side first. If the left information was fresh and clear, it selected `TURN_LEFT`.If the left side was unavailable, it checked the right side and selected `TURN_RIGHT` only when the right information was fresh and clear. 

The stale-message tests were especially important. Even whent the store left or right state still showed `PATH_CLEAR`, the robot stopped after the message became older than three seconds. 

This confirmed that the robot was making decisions using both the sensor state and the reliability of that state. 


## Personal Reflection 

Today I felt that my robot became more intelligent because it was no longer limited to moving foroward or stopping. It could inspect different directions and decide whether to turn left or right. 

I learned that enviroment states and motor commands are different. `PATH_CLEAR` and `OBSTACLE_DETECTED` describe the enviroment, while `MOVE_FORWARD`, `TURN_LEFT`,`TURN_RIGHT`, and `STOP` describe what the robot should do. 

I also understood more clearly why the order of if, elif , and nested conditions matters, When the frony is blocked,the side-direction checks must happen insidw the front-obstacle condition. Otherwise ,Pythom may publish `STOP` before checking whether a safe turn is available. 

The freshness tests made the lesson feel realistic.The stored state did not disappaer when a publisher stopped, but the robot still recognised that eh information had become too old to trust. 

I made several small mistakes with spelling, variable names, indentation,conditions and missing punctuation. Finding and correcting these mistakes helped me understand the program better insted of only looking at finished code. 

Tommorow is my dat off, and I want to rebuolf the ROS2 nodes from scratch without looking at the existing code. My goal is to prove that i can create the nodes, connects the topics, build the package , run the system,and debug it by myself.


Day 19 Summary 

On Day 19, I introduced directional navigation to my ROS2 restaurant delivery robot.

I added front,left,and right directional states, created subscriptions and callbacks for the left and right sensor messages, and added freshness checking for both side directions. 

I created `update_front_state() to combinr camera and LiDAR information safely. The robot now moves forward only when both front sensors confirm `PATH_CLEAR`. 

When the front is blocked, the robot can turn left if the left information is fresh and clear. If the left side is unavailable, it can turn right when the right information is fresh and clear. If no trusted safe direction exists, it stops. 

I added `TURN_RIGHT` support to the motor-control direction exists, node and successfully tested complete communication chain from directional sensor messages to navigation decisions and wheel behaviour.

The final motor commands are: 
    - `MOVE_FORWARD`
    - `TURN_LEFT`
    - `TURN_RIGHT`
    - `STOP`

The most important safety rule remains: 
  > the robot must never move or turn using missing, unknown, or stale sensor information.
