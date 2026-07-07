# Day 13: ROS2 Subscriber and Node-to-Node Communication

## Learning Evidence

* YouTube video: [https://youtu.be/UvBqCoG4nLY]
* ROS2 package: `restaurant_robot_status`
* Publisher node: `robot_status_publisher`
* Subscriber node: `robot_status_subscriber`
* Topic: `/robot_status`
* Message type: `std_msgs/msg/String`

### Code Files

Publisher:

```text
projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status/robot_status_publisher.py
```

Subscriber:

```text
projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status/robot_status_subscriber.py
```

Package configuration:

```text
projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/setup.py
```

## Goal

The goal of Day 13 was to create a second ROS2 node that subscribes to the `/robot_status` topic and receives the robot status published by the Day 12 publisher node.

I wanted to understand how two separate ROS2 nodes communicate with each other using a topic.

The communication flow was:

```text
robot_status_publisher
        ↓ publishes
/robot_status
        ↓ carries the message
robot_status_subscriber
        ↓ receives
receive_status() callback
```

## Environment and Project Checks

Before changing the code, I checked that ROS2 Jazzy was active:

```bash
printenv ROS_DISTRO
```

Output:

```text
jazzy
```

I moved to the repository root:

```bash
cd ~/mission-korea
```

I checked my current location:

```bash
pwd
```

Output:

```text
/home/pradip/mission-korea
```

I checked that the ROS2 workspace still existed:

```bash
ls projects/ros2-restaurant-delivery-robot/ros2_ws
```

The workspace contained:

```text
build
install
log
src
```

I checked the existing ROS2 package:

```bash
ls projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status
```

I also checked Git before making changes:

```bash
git status
```

The repository was clean and up to date with the remote `main` branch.

## Day 12 Publisher Review

The existing publisher node publishes the robot status:

```text
SAFETY_CHECK
```

The publisher sends this message through:

```text
/robot_status
```

It uses the message type:

```text
std_msgs/msg/String
```

The publisher runs a timer every second. The timer calls the `publish_status()` callback, which creates and publishes a new message.

```text
One-second timer
        ↓
publish_status() callback
        ↓
Create String message
        ↓
Store SAFETY_CHECK in message.data
        ↓
Publish the message
```

## Publisher, Topic, and Subscriber

My current understanding is:

* A node is one ROS2 robot worker.
* A publisher sends information.
* A subscriber receives information.
* A topic is the communication channel between nodes.
* A message is the information travelling through the topic.

For Day 13:

```text
Publisher node:
robot_status_publisher

Topic:
 /robot_status

Subscriber node:
robot_status_subscriber

Message type:
std_msgs/msg/String
```

The publisher and subscriber must use the same topic name and a compatible message type.

The publisher sends the message, the topic carries it, and the subscriber receives it.

## What Is a Callback?

A callback is a prepared robot reaction that ROS2 calls when an event happens.

For the publisher:

```text
Event:
One second passes

Reaction:
ROS2 calls publish_status()
```

For the subscriber:

```text
Event:
A message arrives on /robot_status

Reaction:
ROS2 calls receive_status()
```

I define the callback function, but I do not manually call it every time.

```text
Define function = prepare robot skill
ROS2 calls function = use robot skill when the event happens
```

The subscriber callback receives the complete ROS2 message object.

The actual robot status is stored inside:

```python
message.data
```

For this project:

```text
message.data = SAFETY_CHECK
```

## Subscriber Node

I created a new file:

```text
robot_status_subscriber.py
```

The subscriber uses these imports:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
```

The subscriber class inherits from the ROS2 `Node` class:

```python
class RobotStatusSubscriber(Node):
```

Inside `__init__()`, I gave the node its ROS2 name:

```python
super().__init__('robot_status_subscriber')
```

I created the subscription using:

```python
self.subscription = self.create_subscription(
    String,
    'robot_status',
    self.receive_status,
    10
)
```

The four subscription settings are:

```text
String
→ Expected message type

robot_status
→ Topic to listen to

self.receive_status
→ Callback ROS2 should call

10
→ Message queue depth
```

I passed:

```python
self.receive_status
```

without parentheses because I was giving ROS2 the prepared function.

Writing:

```python
self.receive_status()
```

would try to call the function immediately.

## Subscriber Callback

The callback receives the incoming message and logs its data:

```python
def receive_status(self, message):
    self.get_logger().info(
        f'Received robot status: {message.data}'
    )
```

The callback flow is:

```text
SAFETY_CHECK arrives
        ↓
ROS2 calls receive_status()
        ↓
The message is passed into the message parameter
        ↓
message.data is read
        ↓
The status is logged in the terminal
```

## Main Function

The `main()` function is outside the class because it controls the complete program.

Its job is to:

```text
Start ROS2
Create the subscriber node
Keep the node alive
Destroy the node when stopped
Shut ROS2 down safely
```

The important line is:

```python
rclpy.spin(node)
```

`rclpy.spin(node)` keeps the subscriber alive and allows ROS2 to call its callback whenever a message arrives.

It does not stop after receiving one message.

It keeps waiting for more messages until I stop the program using:

```text
Ctrl + C
```

## Registering the Subscriber Executable

Creating the Python file was not enough. I also had to register it inside `setup.py`.

The final `console_scripts` section contained:

```python
entry_points={
    'console_scripts': [
        'robot_status_publisher = restaurant_robot_status.robot_status_publisher:main',
        'robot_status_subscriber = restaurant_robot_status.robot_status_subscriber:main',
    ],
},
```

The subscriber entry means:

```text
robot_status_subscriber
→ Executable name used with ros2 run

restaurant_robot_status
→ Python package name

robot_status_subscriber
→ Python file name

main
→ Function ROS2 starts
```

The command structure is:

```text
ros2 run <package_name> <executable_name>
```

The subscriber command is:

```bash
ros2 run restaurant_robot_status robot_status_subscriber
```

## Syntax Checks

Before building, I checked the Python syntax of the subscriber:

```bash
python3 -m py_compile projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status/robot_status_subscriber.py
```

I also checked `setup.py`:

```bash
python3 -m py_compile projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/setup.py
```

Both commands produced no output.

No output meant the Python syntax checks passed.

## Building the Package

I moved into the ROS2 workspace:

```bash
cd ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws
```

I built only the package I changed:

```bash
colcon build --packages-select restaurant_robot_status
```

Build output:

```text
Starting >>> restaurant_robot_status
Finished <<< restaurant_robot_status

Summary: 1 package finished
```

I then sourced the updated workspace:

```bash
source install/setup.bash
```

Sourcing teaches the current terminal about the newly built package and executables.

I checked the registered executables:

```bash
ros2 pkg executables restaurant_robot_status
```

Output:

```text
restaurant_robot_status robot_status_publisher
restaurant_robot_status robot_status_subscriber
```

The first part is the package name, and the second part is the executable name.

## Running Both Nodes

### Terminal 1 — Publisher

I ran:

```bash
ros2 run restaurant_robot_status robot_status_publisher
```

The publisher repeatedly displayed:

```text
Publishing robot status: SAFETY_CHECK
```

The publisher continued because its one-second timer repeatedly called `publish_status()`.

### Terminal 2 — Subscriber

In a new terminal, I moved into the workspace and sourced it again:

```bash
cd ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws
source install/setup.bash
```

I ran:

```bash
ros2 run restaurant_robot_status robot_status_subscriber
```

The subscriber displayed:

```text
Received robot status: SAFETY_CHECK
```

This confirmed that the subscriber was receiving the status created by the publisher.

The subscriber did not create `SAFETY_CHECK`. It received it through `/robot_status`.

## Inspecting the ROS2 System

I opened Terminal 3 and sourced the workspace.

I checked the active nodes:

```bash
ros2 node list
```

Output:

```text
/robot_status_publisher
/robot_status_subscriber
```

This confirmed that both robot workers were active.

I inspected the topic:

```bash
ros2 topic info /robot_status
```

Output:

```text
Type: std_msgs/msg/String
Publisher count: 1
Subscription count: 1
```

### Why Publisher Count Was 1

Publisher count was `1` because only one node was publishing messages to `/robot_status`:

```text
/robot_status_publisher
```

### Why Subscription Count Was 1

Subscription count was `1` because only one node was listening to `/robot_status`:

```text
/robot_status_subscriber
```

Before creating the subscriber, the subscription count would have been `0`.

## Inspecting the Publisher Node

I ran:

```bash
ros2 node info /robot_status_publisher
```

The important section was:

```text
Publishers:
  /robot_status: std_msgs/msg/String
```

This confirmed that the publisher node sends `String` messages through `/robot_status`.

The publisher also had ROS2 system publishers such as:

```text
/parameter_events
/rosout
```

## Inspecting the Subscriber Node

I ran:

```bash
ros2 node info /robot_status_subscriber
```

The important section was:

```text
Subscribers:
  /robot_status: std_msgs/msg/String
```

This confirmed that the subscriber listens to `/robot_status` and expects a `String` message.

The subscriber also published to `/rosout` because it used:

```python
self.get_logger().info(...)
```

## Restaurant Robot Meaning

In a real restaurant delivery robot, the publisher could announce the robot’s current state:

```text
IDLE
SAFETY_CHECK
MOVING
DELIVERING
RETURNING
ERROR
```

Other nodes could subscribe to this information.

Examples include:

```text
Dashboard node
→ Displays the current robot status

Logger node
→ Saves the status history

Safety monitor
→ Watches for dangerous or unexpected states

Mission controller
→ Uses the status to decide the next operation
```

Not every function must become a separate ROS2 node. Nodes should be separated when they represent useful independent responsibilities or components.

## Problems and Corrections

During the lesson, I made several spelling and syntax mistakes.

Examples included:

```text
relpy instead of rclpy
Suscriber instead of Subscriber
slef instead of self
Node written as note
create_subscriptioin instead of create_subscription
RobotStatusSubscription instead of RobotStatusSubscriber
```

I also forgot:

* closing quotes;
* colons after class or function definitions;
* correct indentation;
* double underscores around `__init__`;
* the subscriber executable inside `setup.py`.

I fixed these mistakes by reading the exact error, checking spelling carefully, and comparing the name I called with the class I had defined.

I also cleaned the formatting of the `console_scripts` section so the package looked more professional.

## Memory and Learning Reflection

I understood the communication logic better than I remembered the exact ROS2 syntax.

At first, I tried rebuilding the subscriber from memory. I realised that trying to memorise every line was not the best learning method for me.

The more important understanding is:

```text
Create node
Prepare subscription
Wait for messages
Run callback
```

The subscriber needs to know:

```text
Message type
Topic name
Callback reaction
Queue depth
```

I can check exact ROS2 syntax from my previous code, notes, autocomplete, or official documentation when needed.

Professional programmers do not memorise every command and function perfectly. They understand the system, recognise patterns, know what they need, and verify syntax when necessary.

Repeated use in future projects will naturally improve my memory.

## What I Learned

Today I learned:

* how to create a second ROS2 Python node;
* how to create a subscription;
* how a subscriber receives messages;
* how ROS2 automatically calls subscriber callbacks;
* why callback functions are passed without parentheses;
* how `message.data` contains the actual `String` information;
* how `rclpy.spin(node)` keeps a subscriber alive;
* why publishers and subscribers must use matching topic names and message types;
* how to register multiple executables in `setup.py`;
* how to build only one ROS2 package;
* why the workspace must be sourced after rebuilding;
* why each new terminal must source the workspace;
* how to run publisher and subscriber nodes in separate terminals;
* how to inspect nodes and topics;
* why publisher count was `1`;
* why subscription count was `1`;
* how to use Python syntax checks before building;
* why understanding patterns is better than blindly memorising code.

## Final Communication Flow

My final understanding is:

```text
The robot_status_publisher creates a String message.

The status SAFETY_CHECK is stored in message.data.

The publisher sends the message through /robot_status.

The robot_status_subscriber listens to the same topic using the same message type.

When the message arrives, ROS2 automatically calls receive_status().

The callback reads message.data and logs the received robot status.
```

## Day 13 Result

Day 13 was completed successfully.

I created, built, ran, and inspected my first ROS2 subscriber node.

The publisher and subscriber successfully communicated through `/robot_status`.

```text
robot_status_publisher
        ↓
/robot_status
        ↓
robot_status_subscriber
        ↓
Received robot status: SAFETY_CHECK
```

This was my first working ROS2 node-to-node communication system.

## Git Status Before Final Commit

Expected Day 13 files:

```text
Modified:
projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/setup.py

New:
projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status/robot_status_subscriber.py

New:
learning-log/2026/Day-13-ros2-subscriber/day-13-notes.md
```
