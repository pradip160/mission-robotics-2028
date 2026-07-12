#Day 17: ROS2 Muntiple Sensor Inputs and Sensor Fusion 

- YouTube video: [https://youtu.be/F0cAd8slHHM]
- Code files:
    - `lidar_obstacle_publixhse.py`
    - `navigation_obstacle_subscriber.py`
    - `setup.py`
- Topic: Multiple sensor inputs and simulated sensor fusion using ROS2 

## Learning Evdience 

## Goal 
At the beginnig, I did not fully understand what today's goal was. I followed the lesson step by step and gradually understood why we were adding another sensor node.By the end. I learned that one ROS2 node can subscribe to muntiple sensor topics, compare their information,and publish a motor command. I also understood that the robot should only move when both sensors confirm that the path is clear.

## Architecture
Camera Publisher ──→ /obstacle_status ──┐
                                        │
                                        ↓
                               Navigation Node
                                        ↓
                                  /motor_command
                                        ↓
                              Motor Control Node
                                        ↑
                                        │
LiDAR Publisher ───→ /lidar_status ─────┘

The camera and LiDAR provide different types of information. A camera can help the robot reconuse what an object is, while LiDAR measures the distance between the robot and nearby objects. In our simulation,both sensors send simplified status messages through separate ROS2 topics.

The camera publisher sends information through /obstacle_status, while the LiDAR publisher sends information through /lidar_status. The navigation node subscribers to both and stores the lastest state from each sensor. It compares the information received from both sensors, makes a decision based in their conditions, and then publishes the selectes instruction through /motor_command to the motor-control node. 
 

## What I Built 
I built a new LiDAR publisher node to simlate muntiple sensot input in the robot system. The LiDAR publsher sends sensor information to the navigation node through the `/lidar_status` topic.

The navigation nodes receives information from both the camera and LiDAR, compares their latest states, and converts the reasult into a motor command that the robot can understand. It then publishers the command through `/motor_command`, and the motor-control  subscriber receives it and simulates the movement of the robot's wheels'
 
## Senosr-Fusion Safety Logic 
If the camera or LiDAR does not provide ant input, or if either sensor state is `UNKNOWN`, the robot should stop. Uncertainty is dengerous in robotics becasue the robot should never move without enough reliable information. 

If eaither the camera or LiDAR detects an obstacle, the robot should also stop. A danger detected by even one sensor could cause harm to the robot, nearby people, or surrounding objects, so one obstacle singal is enough to trigger a safe stop. 

The robot should move forward only when both the camera reports `PATH_CLEAR` and the LiDAR reports `PATH_CLEAR`. Both sensors must agree before the robot is allowed to continue moving. 

## Testing and Reasults
I first tested the LiDAR publisher by itself. It successfully published alternating sensor every two seconds:
 - `PATH_CLEAR`
 - `OBSTACLE_DETECTED`
I then tested the navigation node using manual ROS2 topic messages. 

When the camera reported `PATH_CLEAR` but thr LiDAR state was still `UNKNOWN`, the navigation node published:
STOP

This conformed that the robot does not move when sensor information is incomplete.

When both the camera and LiDAR reported `PATH_CLEAR`, the navigation node published:
MOVE_FORWARD

The motor-control subscriber received this command and displayed that both wheels were moving forward at the same speed.

I also tested a disagreement between the sensors. The camera reported `PATH_CLEAR`, while the LiDAR reported `OBSTACLE_DETECTED`. The navigation node correctly published: 

STOP

The motor-control node then confirmed that both wheeks stopped safely.

These tests confirmes that the complete pipeline worked:

Camera + LiDAR -> Navigation decision -> Motor command -> Motor-control reaction
## ROS2 Inspection 
I used ROS2 inspection commands to check whether the nodes and topics were connected correctly.

I used:

ros2 node list

This confirmed that the navigation node, motor-control node, and LiDAR publisher were running.

I also used:

ros2 topic list

This showed the main communication topics:

/obstacle_status
/lidar_status
/motor_command

Then I inspected the navigation node using:

ros2 node info /navigation_obstacle_subscriber

The result confirmed that the navigation node subscribed to both sensor topics:

/lidar_status
/obstacle_status

It also confirmed that the same navigation node published motor instructions through:

/motor_command

Finally, I used:

ros2 topic info /lidar_status
ros2 topic info /motor_command

Both topics showed one publisher and one subscriber. This confirmed that the sensor, navigation, and motor-control nodes were connected and communicating correctly.
## Problems I Faced and Fixed 
While modifiying the navigation node, I accidentally kept some of the old Day 16  decision logic inside the receive_obstacle() callback. This caused duplicated code and undefined variables. I fixed it by keeping the callback reponsinle for only saving the camera state and calling the shared `decide_navigation()` function.

I also made several small syntax mistakes, including using = instead of == inside a condition, writing dara instead of data, and formatting the logger incorrectly. I used python3 -m py_compile to find and correct these errors before rebuilding the ROS2 package.

At first, I also used the wrong file path when running the syntax-check command. I learned that the correct relative path depends on which directory I am currently inside.

When I stopped the LiDAR node with Ctrl+C, ROS2 displayed a shutdown traceback. The publisher itself was working, but the ROS2 context was being shut down twice. I fixed this by replacing rclpy.shutdown() with rclpy.try_shutdown(), and the node then stopped cleanly.

Finally, I checked for accidental build, install, log, and __pycache__ folders inside the source package. I removed the Python cache folders and confirmed that the package was clean before preparing it for GitHub.
## What I Learned 
Today I learned that one ROS2 node can have multiple subscrptions and can also publish message at the same time. The navigation node listens to both `/obstacle_status` and `/lidar_status`, compares the latest information, and publishes a motor command through `/motor_command`.

I learned why different sensors are useful in robotics. A camera can help identify objects, while LiDAR can measure distance and detect whether something is blocking the robot's path.Using more than one sensoe makes the robot's decision safer than depending on only one source.

I also learned that callbacks should have small and clear responsibilities. The camera callback stores the latest camera state. the LiDAR callback stores the latest LiDAR state, and both callbacks call the shared `decide_navigation()` function. 

The most important saftey lesson was that one danger signal is enough to stop the robot, but both sensor must agree before the robot moves forward. I also improved my understanding of ROS2 topic insepction, package biuiling, workspace sourcing,syntax checling, and clean code shutdown.

## Personal Reflection 
Today I did not fully understand the goal at the beginning,I depended a lot on guidance while building the new LiDAR publisher and modifying the navigation node. However,as I tested each part, the purpose became clearer

I understood that learning robotics is not only about remembering ROS2 syntax. It is also about understanding how separate nodes communicate, how sensor information is compared, and how safety decisions are made before the robot moves.

I made several mistakes while editing the code, but fixing them helped me understand the structure better. I now have a clearer idea of how a camera node, LiDAR node, navigation node, and motor-control node can work together as one robot system.

I still need more repetition before I can write all of this independently, but I am improving by recognising the same ROS2 patterns again and again. Today’s work showed me that I can continue progressing even when I do not understand everything immediately.
