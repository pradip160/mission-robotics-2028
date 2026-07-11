# Day 16: ROS2 Navigation Decisions and Motor Commands

## Learning Evidence

* **YouTube Video:** *[https://youtu.be/sHsnsdwQyYo]*
* **Code Files:**

  * `projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status/navigation_obstacle_subscriber.py`
  * `projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status/motor_control_subscriber.py`
* **Topic:** ROS2 Navigation Decisions, Publisher & Subscriber in One Node, Motor Commands, Multi-Node Communication

---

# Goal

Today's goal was to improve the restaurant delivery robot by separating navigation decisions from motor actions.

Previously, the navigation node only printed its decision after receiving sensor information.

Today, I extended the communication pipeline so that the navigation node now publishes movement commands for a dedicated motor-control node to receive.

This follows the modular design used in real ROS2 robots, where different nodes are responsible for different parts of the robot.

---

# What I Built

## Existing Camera Node

The camera node continued publishing sensor information through:

`/obstacle_status`

Possible sensor states:

* `OBSTACLE_DETECTED`
* `PATH_CLEAR`
* `PERSON_DETECTED`

The camera node only reports what it detects. It does not decide how the robot should move.

---

## Navigation Node

I modified the existing navigation node so that it now performs two jobs.

It:

* subscribes to `/obstacle_status`
* publishes movement commands through `/motor_command`

This taught me that a single ROS2 node can be both:

* a subscriber
* a publisher

The navigation node now converts sensor information into movement commands.

Sensor State → Motor Command

* `OBSTACLE_DETECTED` → `TURN_LEFT`
* `PATH_CLEAR` → `MOVE_FORWARD`
* `PERSON_DETECTED` → `STOP_AND_WAIT`
* Unknown state → `STOP`

The navigation node is responsible for making decisions, not controlling hardware directly.

---

## Motor-Control Node

Today I created a new node:

`motor_control_subscriber.py`

This node subscribes to:

`/motor_command`

It converts movement commands into simulated wheel behaviour.

Current simulated reactions:

* `MOVE_FORWARD`

  * both wheels move forward at the same speed

* `TURN_LEFT`

  * left wheel slows down
  * right wheel moves faster

* `STOP_AND_WAIT`

  * both wheels stop and wait

* `STOP`

  * both wheels stop safely

Unknown commands produce a warning and stop safely.

---

**Navigation Decision**

Chooses the safest movement after analysing sensor information.

---

**Motor Command**

Tells the motor-control system what movement should happen.

Examples:

* `MOVE_FORWARD`
* `TURN_LEFT`
* `STOP_AND_WAIT`
* `STOP`

---

**Motor Action**

The motor-control node converts commands into wheel behaviour.

In future robots, these commands will become real wheel speeds instead of log messages.

---

# Differential Drive

I learned how a differential-drive robot turns.

Forward

* left wheel forward
* right wheel forward
* same speed

Left Turn

* left wheel slower
* right wheel faster

Stop

* both wheel speeds become zero

Emergency Stop

* stop safely as quickly as possible

---

# Testing Completed

I tested the system using:

* automatic camera publishing
* manual publishing using:

```bash
ros2 topic pub --once /obstacle_status std_msgs/msg/String "{data: 'PERSON_DETECTED'}"
```

I also tested:

```text
SENSOR_ERROR
```

to confirm that the navigation node publishes `STOP` and the motor-control node performs a safe stop.

---

# ROS2 Commands Practised

```bash
ros2 topic echo /obstacle_status
```

```bash
ros2 topic echo /motor_command
```

```bash
ros2 topic info /obstacle_status
```

```bash
ros2 topic info /motor_command
```

```bash
ros2 node list
```

```bash
ros2 node info /navigation_obstacle_subscriber
```

```bash
ros2 node info /motor_control_subscriber
```

I also confirmed that `ros2 topic echo` temporarily increases the subscriber count because it behaves as a subscriber while listening to the topic.

---

# Reflection

Today was one of the biggest steps in my ROS2 learning journey.

I built my first multi-node communication pipeline where each node has a separate responsibility.

The camera senses the environment.

The navigation node analyses the information and makes a decision.

The motor-control node converts that decision into wheel actions.

I also realised that I can now recognise most ROS2 node patterns and understand how information flows through the system. I still need more practice writing new code from memory, but I understand the architecture much better than when I started. My focus is to keep building new robotics concepts while gradually improving my coding confidence through repetition.

This modular design is how real autonomous robots are built, and today helped me understand why separating sensing, decision-making, and actuation makes robotic systems easier to maintain, test, and expand.
