## Learning Evdience 

- YouTube video: []
- Publisher node: `camera_obstacle_publisher`
- Subscriber node: `navigation_obstacle_subscriber`
- Topic: `/obstacle_status`
- Message type: `std_msgs/msg/String`

## Goal

I wanted to simulate how actual robot nodes communicate with each other. I created a camera node that publishes and obstacle message and a navigation subscriber node that receives the message and react on it.

In my current code,`camera_obstacle_publisher` acts as the publisher, `while navigation_obstacle_subscriber` receives the message and logs a decision to change direction. 

Today, I only built simulation. These nodes are not connected to real camera, navigation system or motor control yet.

## What I Learned

I learned how publisher and subscriber nodes work and communicate with each other in ROS2. A publisher sends messages through a topic, and a subscriber receives those messages from the same topic.

For communication to work, both nodes must use the same topic name and a compatiable message type. Without this match, the publisher and subscriber cannot communicate correctly. 

Topics act as communication channels between ROS2 nodes. There can also be muntiple publishers and muntiple subscribers connected to the same topic at the same time. 

I also learned about callbacks. A callback is a prepared robot reaction that ROS2 calls automatically when an event happens. In this project, whem the navigation subscriber receives Obstacle_detected, ROS2 automatiaclly calls receive_obstacle(message). The callback then checks message.data and logs the decision to change direction.

I also learned that ros2 topic echo makes the terminal act like a temporary subscriber. We can use it to quickly check whether a publisher is sending message correctly before creating or testing a permenant subscriber node.


## ROS2 Communication Flow

First, the camera_obstacle_publisher simulates detecting and obstacle and prepares a String messgae containing OBSTACLE_DETECTED. 

The publisher sends this message through the /obstacle-status topic. The subscriber must listen to the same topic and use the same compitable message type to receive it.

The navigation_obstacle_subscriber receives the message, and ROS2 automatically calls the receive_obstacle(message) callback. The callback checks message.data and logs.

Obstacle detected - changing direction

After reacting, the subscriber continues listining for a new messages. The nodes shutdown safely only when we stop them using Ctrl + C.

## Testivng and Verification

For testing, I used the cat command to display the complete Python file and check the overall structure. I also used sed -n to display only specific lines, which helped me inspect smaller sections without opening the whole file. 

After correcting spelling, indenataion, topic names, and ROS2 syntax, I built the package using:

`colon build --packages-select restaurant_robot_status`

The successful build conformed that the package was installed without build errors. I then sourced the workspaces using:

`source install/setup.bash`

Sourcing updated the current terminal enviroment so ROS2 could discover the latest package and the new execuatable.

Before running the permanent nacvigation subscriber, I used:
`ros2 topic echp/ obstacle_status`

This  made the terminal act as a temporary subscriber and conformed that the camera publisher was sending OBSTACLE_DETECTED.

After running both nodees,I used a third terminal to inspect the ROS2 system with
- `ros2 node list`
- `ros2 node info /camera_obstacle_publisher`
- `ros2 node info /navigation_obstacle_subscriber` 
- `ros2 topic info /obstacle_status`

These commanda conformed that both nodes were runnig, using the same topic and message type, and communicating correctly. The topic information showed one publisher and one subscriber:

`Publisher count: 1`
`Subscriber count: 2`


## Problems and fixes

I faced muntiple problems while building the subscriber node, mainly spelling mistakes, indentation errors, and incorrect terminal commands.

Some of the mistakes included:

- Writing create_subsvrition insted of create_subscription
- Misspelling 0BSTACLE_DETECTED
- Writing the logger incorrectly insted of using self.get_l0gger().info()
- Writing destory node() insted of destroy_node()
- Misspelling the package name in setup.py
- Incorrect indentation inside __init__() and the callback function

I checked the file using cat and sed -n, correct each mistake one by one, rebuilt the package, sourced the workplace again, and tested both nodes.

After debugging these problems, the publusher and subscriber communicated successfully, and the system ran smoothly. 

## Reflection

I learned many useful things about ROS2, including how publisher and subscriber nodes work and communicate with each other. I also learned how to create a temporary subscriber using `ros2 topic echo` to check whether a publisher is sending messages correctly.

I learned that I need to run `source install/setup.bash` after building the package and in each new terminal so ROS2 can discover the latest package and executables.

Today, I also learned new ROS2 code patterns. Publisher and subscriber nodes have some similar parts, such as importing ROS2 libraries, creating a node class, using `main()`, and calling `rclpy.spin(node)`. However, their main responsibilities are different: the publisher creates and sends messages, while the subscriber listens for messages and reacts through a callback.

This lesson helped me understand that small spelling and indentation mistakes can stop the whole node from working. By debugging each problem step by step, I successfully built working obstacle communication between two ROS2 nodes.

