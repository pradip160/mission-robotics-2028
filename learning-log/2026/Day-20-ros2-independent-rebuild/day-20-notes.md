# Day 20: Independent ROS2 System Rebuild

## Learning Evidence

* YouTube video: [https://youtu.be/BrvU2jHEflo]
* ROS2 package: `restaurant_robot_practice`
* Practice workspace: `/home/pradip/mission-korea-day20-practice/ros2_ws`
* Main topic: Rebuilding a multi-sensor navigation and motor-control system independently

## Goal

I wanted to understand my code and how the whole system works more clearly. I realised that moving forward and continuously adding new features without properly understanding the basics would not help me learn.

Therefore, I created a separate practice workspace to test myself and find out whether I had actually understood what I learned during the previous ROS2 lessons.

My goal was to rebuild the sensor publishers, navigation node, sensor freshness system, and motor-control subscriber without changing my main restaurant robot project.

## System Architecture

I created six ROS2 nodes inside the `restaurant_robot_practice` package.

### Sensor Publisher Nodes

* `camera_obstacle_publisher` publishes camera information to `/obstacle_status`.
* `lidar_obstacle_publisher` publishes LiDAR information to `/lidar_status`.
* `left_obstacle_publisher` publishes left-side information to `/left_status`.
* `right_obstacle_publisher` publishes right-side information to `/right_status`.

The sensor publishers use the `std_msgs/msg/String` message type. During testing, they published states such as:

* `PATH_CLEAR`
* `OBSTACLE_DETECTED`

### Navigation Node

The `navigation_obstacle_subscriber` subscribes to:

* `/obstacle_status`
* `/lidar_status`
* `/left_status`
* `/right_status`

The navigation node stores:

* The latest state received from each sensor
* The time when each sensor message was received
* Whether each sensor message is fresh or stale

After checking the sensor information, navigation publishes one of the following commands to `/motor_command`:

* `MOVE_FORWARD`
* `TURN_LEFT`
* `TURN_RIGHT`
* `STOP`

### Motor-Control Node

The `motor_control_subscriber` subscribes to `/motor_command`.

It receives the navigation command and converts it into simulated wheel behaviour.

### Communication Flow

```text
Camera publisher ──────> /obstacle_status ──┐
LiDAR publisher ───────> /lidar_status ─────┤
Left publisher ────────> /left_status ──────┼──> Navigation
Right publisher ───────> /right_status ─────┘
                                                 │
                                                 ▼
                                          /motor_command
                                                 │
                                                 ▼
                                      Motor-control subscriber
```

This architecture separates sensing, decision-making, and motor behaviour into different ROS2 nodes.

## Navigation Decision Logic

The navigation node receives information from the camera, LiDAR, left sensor, and right sensor. It stores the latest state and timestamp from each sensor before making a movement decision.

The decision rules are:

* If the camera or LiDAR message is missing, the robot publishes `STOP`.
* If the camera or LiDAR message is stale, the robot publishes `STOP`.
* If either front sensor state is `UNKNOWN`, the robot publishes `STOP`.
* If both the camera and LiDAR report `PATH_CLEAR`, the robot publishes `MOVE_FORWARD`.
* If the front is blocked and the left sensor is fresh and reports `PATH_CLEAR`, the robot publishes `TURN_LEFT`.
* If the left route is unavailable but the right sensor is fresh and reports `PATH_CLEAR`, the robot publishes `TURN_RIGHT`.
* If no safe route is available, the robot publishes `STOP`.

The robot checks the left side before the right side, so the left route has priority when both directions are available.

## Sensor Freshness Safety

Each sensor message stores the ROS2 time when it was received. The navigation node compares the current time with the last message time to calculate the age of the sensor data.

I set the sensor timeout to three seconds. If a sensor does not publish a new message within three seconds, its data is marked as stale.

The robot must not continue moving using an old sensor message because the environment may have changed. For example, a side sensor may previously have reported `PATH_CLEAR`, but an obstacle may have entered that area after the sensor stopped working.

In uncertain situations, the robot stops instead of making a movement decision using outdated information.

## Motor-Control Logic

The `motor_control_subscriber` subscribes to the `/motor_command` topic and converts navigation commands into simulated wheel actions.

The commands are interpreted as follows:

* `MOVE_FORWARD` → both wheels move forward at the same speed.
* `TURN_LEFT` → the left wheel slows down while the right wheel moves faster.
* `TURN_RIGHT` → the right wheel slows down while the left wheel moves faster.
* `STOP` → both wheels stop safely.
* `STOP_AND_WAIT` → both wheels stop and wait.
* Unknown command → the motor-control node prints a warning and uses safe stopping behaviour.

This separates the navigation decision from the physical motor behaviour. The navigation node decides what the robot should do, while the motor-control node decides how the wheels should perform that command.

## Testing and Results

### Test 1: No Sensor Messages

I started the navigation node without running any sensor publishers.

**Result:** The navigation node published `STOP`.

This confirmed that the robot does not move when the required sensor information is missing.

### Test 2: Camera and LiDAR Clear

I ran both the camera and LiDAR publishers. Both publishers sent `PATH_CLEAR`.

**Result:** The navigation node published `MOVE_FORWARD`.

The motor-control subscriber received the command and displayed:

```text
Both wheels moving forward at the same speed
```

This confirmed that the complete communication chain worked correctly.

### Test 3: Camera Message Became Stale

I stopped the camera publisher while keeping the LiDAR publisher running.

The navigation node initially continued using the recent camera message. After the camera message became older than three seconds, it was marked as stale.

**Result:** The navigation command changed from `MOVE_FORWARD` to `STOP`.

This confirmed that the robot does not continue trusting an old `PATH_CLEAR` message.

### Test 4: Front Obstacle and Left Side Clear

I published `OBSTACLE_DETECTED` on the camera topic while the LiDAR remained fresh. I also ran the left-side publisher with `PATH_CLEAR`.

**Result:** The navigation node published `TURN_LEFT`.

The motor-control subscriber displayed:

```text
Left wheel slow down and right wheel move faster
```

This confirmed that the robot could choose an available side route when the front path was blocked.

### Test 5: Left Side Stale and Right Side Clear

I stopped the left-side publisher and started the right-side publisher.

After the left message became stale, the right sensor continued sending `PATH_CLEAR`.

**Result:** The navigation node published `TURN_RIGHT`.

The motor-control subscriber displayed:

```text
Right wheel slow down and left wheel move faster
```

This confirmed that the robot could use the right route when the preferred left route was unavailable.

### Test 6: Both Side Sensors Stale

I stopped the right-side publisher while the front remained blocked.

After the right message became older than three seconds, both side routes were unavailable.

**Result:** The navigation node published `STOP`.

The motor-control subscriber displayed:

```text
Both wheels stop safely
```

This confirmed that the final safety fallback worked correctly.

## Debugging and Problems Faced

During testing, I noticed that the navigation output repeatedly changed between `MOVE_FORWARD`, `STOP`, and `TURN_LEFT`.

I used:

```bash
ros2 topic info /obstacle_status -v
```

The command showed that two different nodes were publishing to `/obstacle_status`:

* The original camera publisher was publishing `PATH_CLEAR`.
* A manual ROS2 command was publishing `OBSTACLE_DETECTED`.

The navigation node was receiving conflicting sensor states, so its decision kept changing.

I stopped the original camera publisher and kept only one publisher on the topic. After that, the navigation and motor-control outputs became consistent.

This taught me that unexpected robot behaviour may not always come from the decision logic. It can also happen because multiple nodes are publishing conflicting information on the same topic.

I also corrected several coding mistakes during development, including:

* Using `create_subscriber()` instead of `create_subscription()`
* Writing `/motor_status` instead of `/motor_command`
* Misspelling `self` as `slef`
* Using subtraction `-` instead of assignment `=`
* Misspelling `destroy_node()`
* Using `=` instead of `==` in the `if __name__` condition
* Using multiple separate `if` statements instead of an `if/elif/else` chain
* Placing code at the wrong indentation level
* Misspelling `STOP_AND_WAIT`

These errors helped me understand how small syntax and logic mistakes can affect the whole ROS2 system.

## Commands Practised

```bash
colcon build --packages-select restaurant_robot_practice
source install/setup.bash

ros2 pkg executables restaurant_robot_practice

ros2 run restaurant_robot_practice camera_obstacle_publisher
ros2 run restaurant_robot_practice lidar_obstacle_publisher
ros2 run restaurant_robot_practice left_obstacle_publisher
ros2 run restaurant_robot_practice right_obstacle_publisher
ros2 run restaurant_robot_practice navigation_obstacle_subscriber
ros2 run restaurant_robot_practice motor_control_subscriber

ros2 topic echo /motor_command
ros2 topic echo /lidar_status --once

ros2 topic info /obstacle_status
ros2 topic info /obstacle_status -v

ros2 topic pub -r 1 /obstacle_status std_msgs/msg/String "{data: 'OBSTACLE_DETECTED'}"

python3 -m py_compile src/restaurant_robot_practice/restaurant_robot_practice/navigation_obstacle_subscriber.py

python3 -m py_compile src/restaurant_robot_practice/restaurant_robot_practice/motor_control_subscriber.py
```

## What I Learned

Today I learned how to rebuild a ROS2 system from an empty workspace instead of only modifying my previous project.

I learned how to:

* Create a ROS2 Python workspace and package
* Create and register several publisher and subscriber nodes
* Connect nodes using ROS2 topics
* Store the latest sensor state inside callbacks
* Store the time when each sensor message was received
* Calculate message age using ROS2 time
* Mark sensor information as fresh or stale
* Make safe navigation decisions using multiple sensors
* Publish movement decisions through `/motor_command`
* Convert navigation commands into simulated wheel actions
* Inspect topics and identify conflicting publishers
* Test the full system using several terminals

I also understood more clearly that a callback receives and stores information, while the decision function uses the stored information to choose the robot’s action.

I learned that defining a function prepares a robot skill, while calling that function uses the prepared skill.

## Personal Reflection

Day 20 was important because I did not want to continue adding new features without properly understanding the system I had already built.

I created a separate workspace and rebuilt the package, publishers, subscribers, navigation logic, sensor freshness system, and motor-control node. I still needed guidance and made several mistakes, but I was able to understand the purpose of each part and correct the errors step by step.

The most important lesson was that safety should always have the highest priority. The robot must not move when sensor information is missing, unknown, stale, or conflicting.

I also learned that debugging is not only about correcting Python syntax. I had to inspect the ROS2 communication system and discover that two publishers were sending different values on the same topic.

This practice showed me that I have learned the main ideas from the previous ROS2 lessons. I am not fully independent yet, but I now understand the system much better than before.

Rebuilding the system helped me identify which concepts I understood and which areas still require more practice. It gave me more confidence because I did not simply run my old code. I created the nodes again, connected them, tested them, and debugged the communication between them.

## Final Result

I successfully rebuilt and tested a multi-sensor ROS2 navigation system with:

* Four sensor publisher nodes
* One navigation decision node
* One motor-control subscriber
* Sensor state storage
* ROS2 timestamps
* A three-second freshness timeout
* Safe movement decisions
* Complete navigation-to-motor communication

The final robot behaviour was:

* Front clear → `MOVE_FORWARD`
* Front blocked and left clear → `TURN_LEFT`
* Front blocked, left unavailable, and right clear → `TURN_RIGHT`
* Missing, unknown, stale, conflicting, or unsafe information → `STOP`

This Day 20 independent rebuild gave me stronger knowledge of ROS2 publishers, subscribers, topics, callbacks, timestamps, safety logic, navigation decisions, and motor-control communication.
