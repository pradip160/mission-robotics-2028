# Day 35 — Diagnostics and Robot Status Publishing

## Goal

Today I learned how a robot can report **why it is moving, stopping, or not ready**, instead of only sending a motor command.

Previously:

```text
/motor_command → tells the robot what to do
```

Now:

```text
/robot_status → explains the current robot condition and why a decision was made
```

## Custom RobotStatus Message

I created:

```text
RobotStatus.msg
```

Fields:

```text
bool robot_ready
string motor_command
string safety_status
string recovery_state
string reason
```

Example:

```text
robot_ready: false
motor_command: STOP
safety_status: SENSOR_STALE
recovery_state: NORMAL
reason: One or more required sensors are stale
```

## Important Concept

The navigation node is the best place to publish robot status because it already knows:

* sensor freshness
* sensor states
* LiDAR validity and distance
* recovery state
* final motor command

So the motor command tells **what the robot will do**, while robot status explains **why**.

## Robot Status Publisher

I created a `/robot_status` publisher using the custom `RobotStatus` message.

I also created a helper method:

```text
publish_robot_status()
```

The method:

1. creates a `RobotStatus` message;
2. fills all fields;
3. publishes the complete message.

The navigation logic prepares:

```text
robot_ready
safety_status
reason
```

and then publishes them together with the motor command and recovery state.

## Diagnostic States Tested

### Safe path

```text
robot_ready: true
motor_command: MOVE_FORWARD
safety_status: SAFE
recovery_state: NORMAL
reason: Front path is clear
```

### Front obstacle, left clear

```text
motor_command: TURN_LEFT
safety_status: AVOIDING_OBSTACLE
```

### Front obstacle, left blocked, right clear

```text
motor_command: TURN_RIGHT
safety_status: AVOIDING_OBSTACLE
```

### No safe side path

```text
robot_ready: false
motor_command: STOP
safety_status: NO_SAFE_PATH
```

### Invalid distance

```text
robot_ready: false
motor_command: STOP
safety_status: INVALID_DISTANCE
```

### Unknown sensor

```text
robot_ready: false
motor_command: STOP
safety_status: SENSOR_UNKNOWN
```

### Stale sensor

```text
robot_ready: false
motor_command: STOP
safety_status: SENSOR_STALE
```

## Problems I Debugged

* I first wrote `.msg` fields in the wrong format using `=`.
* Correct ROS2 message syntax is:

```text
type field_name
```

* I misspelled `safety_status` as `saftey_status`.
* I accidentally placed `def receive_obstacle()` inside the `if/elif` navigation chain, causing a syntax error.
* LiDAR remained stale because its freshness was not being updated inside `check_sensor_freshness()`.
* During testing I had duplicate and stopped manual sensor publishers.
* I used `ros2 topic info` to check publisher and subscriber counts and find the problem.

## What I Learned

A working robot should not only perform actions. It should also expose its internal condition so a human operator or another system can understand why it made a decision.

Diagnostics make debugging and monitoring much easier.

## Status

```text
RobotStatus custom message          → completed
/robot_status publisher             → completed
Diagnostic helper method            → completed
Navigation integration              → completed
Runtime tests                        → completed
Independent rebuild                 → not tested yet
```

Next:

```text
Day 36 — ROS2 Launch Files
```

