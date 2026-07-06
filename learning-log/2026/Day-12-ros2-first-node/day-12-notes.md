##Day 12: ROS2 Foundation and My First Robot Node 

##Learning Evidence 
- YouTube video = [https://youtu.be/2ZRWCZLwsNM]
- ROS2 workplace : projects/ros2-restaurant-delivery-robot/ros2_ws
- ROS2 packaeg: projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status
- Node file: rstaurant_robot_status/robot_status_publisher.py
- Topic: ROS2 workplaces, packages, nodes, topics, messages, publishers. timers, and terminal inspection

##Goal 
My goal for Day 12 was to begin real ROS2 development. I wanted to understand how My Day11 restaurant robto controller could later communicate through ROS2. 

I also wanted to create my first Python ROS2 node that publishes the current robot status. 

## Enviroment Check
Before installling ROS2,I checked mt operating system and ROS2 enviroment. 

My system information was:
- Ubuntu version: 24.04.1 LST
- Ubuntu codename: noble
- Existing ROS2 installion: not found
- Existing ROS_DISTRO value: empty
- Locale: C.UTF-8

Because I was usning Ubuntu 24.04 Noble, I installed ROS2 Jazzy. 

After installation and enviroment setup, I verified:

ROS2 executable: /opt/ros/jazzy/bin/ros2
ROS_DISTRO: jazzy

I also added the ROS2 jazzy setup command to my .bashrc file so that new terminals automatically reconise ROS2.

## How Day 11 Connects ROS2
On Day 11, my robot controller selected orders, checked battery safety, detectes obstacales, checked tray stability, changed mission states, and saved  mission history inside one python program. 
In ROS2, some parts of this system may later become different nodes that communicate with each other. 

However, I learned that every Python function doesnot need to become a seprate node. Related helper functions can remain together inside one node. 

For example, a future robot system could include:
- an order-management node
- a battery-monotoring node
- a safety-controller node
- a navigation node
- a robot-status node

For Day 12, I created only one small node. 

## ROS2 Concepts I Learned
A ROS2 workplace is the main development area where ROS2 packages are stord and built. 
My workplace is:
ros2_ws

Its source folder is:
ros2_ws/src

## Package 
A ROS2 package is an organised toolbox containing related ROS2 code, dependencies, configuration files, and tests. 

My package is:
restaurant_robot_status

## Node 
A node is one robot worker witn a specific respomnsibility. 

## My node is:
robot_status_publisher,
Its responsibility is to publish channel used BY ROS2 nodes.

## Topic
A topic is a communication channel used by ROS2 nodes. 
My topic is 
/robtoa_status

## Message 
A message is the information travelling through a topic
My nodes published:
SAFETY_CHECK
using the ROS2 message type:
std_msgs/msg/String

## Publisher
A publisher is a node that sends messages through a topic. 
My robot_status_publisher nodes sends robot-state messages through / robot_status

## Suscriber
A suscriber receives message from a topic

I didnot crate a suscriber node today, but this terminal command temporaily acted a suscriber:
ris2 topics echo/ robot_status

##  Communication Flow 
The communicatoin flow i created was: 

robot_status_publisher node
      publishes
saftey_check message
      through
/robot_status topic
      receuved by 
ros2 topic echo 

Terminal 1 kept the publisher node running.
Terminal 2 listined to the topic and conformed that the message was being received.

If Terminal 1 stopped,the publisher stopped sending messages and termial 2 had nothing to recive.

## What I Built

I created a Pytnon ROS2 package using: 
ros2 pkg create --build-type ament_python --license Apache-2.o restaurant_robot_status --dependencies rclpy std_msgs

I then creates 
restaurant_robot_status/robto_status_publisher.py

The node: 
- inherits from the ROS2 Node class
- creates a String publisher
- publishes through the robot_status topic
- uses a one second timer
- publishes the current robot state
- displays the published state using the ROS2 logger

Important Code Understanding

This line prepare the publisher: 

self.publisher_ = self.create_publisher(
     String,
     'robot_status',
     10
     )
This timer calls the publishing function every secound:

self.timer_ = self.create-timer(
    1.0,
    self.publish_status
   )
The publish_status() function contains the actual publishing logic:

message = String()
message.data = 'SAFETY_CHECK'
self.publisher_.publish(message)

My understanding is:

message = String()
 > create an empty ROS2 message 
message.data = 'SAFETY_CHECK'
 > put the robot state inside the message 

self.publisher_.publish(message)
 > send the message through the topic

This line keeps the node alive so that ROS2 can continue processing the timer callback:

rclpy.spin(node)

Build and Run Process

After changing and saving ROS2 code, I learned this workflow:

Chnage code 
> save
> build
> source
> run
> inspect

The main commands were: 

cd ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws

colon build -- packages-selevt restaurant_robot_status

source install/setup.bash

ros2 run restaurant_robot_status robot_status_publisher 


My understanding is :
- Build = prepare the package after changig its code
- Source =  tell the current terminal about the newly built package
- Run = start the robot worker

RIS2 Inspection Commands 
I checked the active node using:
ros2 node lisr
Output:
/robot_status_publisher
I inspected the node using: 
ros2 node info /robot_status_publisher
This conformied that it published: 
/robot_status: std_msg/msg/String
I listed the active topics using: 
ros2 topic list 

Output included: 

/parameter_events
/robot_status
/rosout

I inspected the robot-status topic using:

ros2 topic info /robot_status

Output:

Type: std_msgs/msg/String
Publisher count: 1
Suscriber count: 0

I received the actual message using: 
ros2 topic echo/ robot_status
ros2 topic list

Output included:

/parameter_events
/robot_status
/rosout

I inspected the robot-status topic using:

ros2 topic info /robot_status

Output:

Type: std_msgs/msg/String
Publisher count: 1
Subscription count: 0

I received the actual message using:

ros2 topic echo /robot_status

This matched the one-secound timer used in the node.
Problems and Debugging

I made several small mistakes while creating the node.

Incorrect __init__ spelling

I wrote:

super().__int__()

I corrected it to:

super().__init__()
Incorrect message-type capitalisation

I wrote:

string

I corrected it to:

String

Python is case-sensitive.

Incorrect topic name

I initially used:

robot-status

I changed it to:

robot_status
Replacing the ROS2 message object

I initially wrote:

message = 'IDLE'

This replaced the ROS2 message object with a normal Python string.

I corrected it to:

message.data = 'IDLE'
Shutdown spelling errors

I wrote:

node.destory_node()
relpy.shutdown()

I corrected them to:

node.destroy_node()
rclpy.shutdown()
Robot-state spelling error

I published:

SAFTEY_CHECK

I corrected it to:

SAFETY_CHECK

This taught me that ROS2 publishes exactly the information provided by the program. It does not automatically correct spelling or check whether a robot state is logically valid.

GitHub Structure

I kept the ROS2 package inside the restaurant robot project:

projects/
    ros2-restaurant-delivery-robot/
        ros2_ws/
            src/
                restaurant_robot_status/

I added the generated ROS2 build folders to .gitignore:

ros2_ws/build/
ros2_ws/install/
ros2_ws/log/

These folders are generated during the build process and do not need to be stored in GitHub.

Reflection

Day 12 was my first real experience with ROS2.

I successfully installed ROS2 Jazzy, created a workspace and package, built my first Python node, published a robot state, and inspected the ROS2 communication from a second terminal.

To be honest, I copied many of the installation and terminal commands during the lesson, and I did not understand everything immediately. After reviewing the lesson slowly, I now understand the main communication flow.

A node is one robot worker. A topic is the communication channel. A message is the information travelling through that channel. A publisher sends the message, and a subscriber receives it.

I can now explain that the robot_status_publisher node sends a SAFETY_CHECK message through the /robot_status topic.

I still need more repetition before I can remember the ROS2 commands and package structure independently. My goal is not to pretend that I mastered ROS2 in one day. My goal is to understand the foundation and improve through repeated practice.

This was an important step because my restaurant robot project has now moved from a normal Python simulation into a real ROS2 package and node.
