# Day 25 — ROS2 All-Sensor Navigation Safety Audit

## Objective

Today I audited the navigation node to make sure the robot cannot move using unknown or stale sensor information.

The robot uses four required sensors:

* Camera
* LiDAR
* Left sensor
* Right sensor

My final safety rule is:

> The robot may make a movement decision only when all required sensors are fresh and all required sensor states are known.

I first made and tested the changes in the practice workspace. After the practice version passed all safety tests, I repeated the improvement in the main portfolio package.

---

## Workspaces

### Practice workspace

```text
/home/pradip/mission-korea-day20-practice/ros2_ws
```

Practice package:

```text
restaurant_robot_practice
```

### Main portfolio repository

```text
~/mission-korea
```

Main ROS2 workspace:

```text
~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws
```

Main package:

```text
restaurant_robot_status
```

The practice workspace allowed me to find and fix mistakes safely before touching the portfolio version.

---

## Initial Git Check

Before changing the main package, I checked the main repository:

```bash
cd ~/mission-korea
git status --short --branch
```

Result:

```text
## main...origin/main
```

This showed that the main repository was clean and synchronized with the remote branch before Day 25 changes began.

---

## Robot Architecture

The robot currently uses six ROS2 nodes:

```text
camera_obstacle_publisher
lidar_obstacle_publisher
left_obstacle_publisher
right_obstacle_publisher
navigation_obstacle_subscriber
motor_control_subscriber
```

Important topics include:

```text
/obstacle_status
/lidar_status
/left_status
/right_status
/motor_command
```

The sensor publisher nodes provide information.

The navigation node:

* stores the latest sensor states;
* stores the latest message timestamps;
* calculates whether each sensor is fresh;
* combines camera and LiDAR information into a front state;
* makes the navigation decision;
* publishes a motor command.

The motor-control node receives the motor command and interprets how the wheels should move.

---

## Three Sensor Information Conditions

A sensor can be in three important information conditions.

### 1. No message received

The sensor timestamp is:

```python
None
```

Its state is normally still:

```text
UNKNOWN
```

Its freshness must be:

```text
False
```

### 2. Fresh message

A message arrived recently, and its age is less than or equal to `sensor_timeout`.

Example:

```text
message age = 1.5 seconds
sensor_timeout = 4.0 seconds
```

Result:

```text
fresh = True
```

### 3. Stale message

The sensor published previously, but its latest message is now older than `sensor_timeout`.

Example:

```text
message age = 5.0 seconds
sensor_timeout = 4.0 seconds
```

Result:

```text
fresh = False
```

A sensor can still have an old stored state such as `PATH_CLEAR` while its freshness is false.

The robot must not trust this old state.

---

## Why an Old `PATH_CLEAR` Value Is Dangerous

A sensor may publish `PATH_CLEAR`, and that value remains stored inside the navigation node.

If the sensor later stops publishing, the stored state may still say:

```text
PATH_CLEAR
```

However, the environment may have changed after the last message. A person, chair, trolley, or another obstacle may now be in the robot’s path.

Therefore:

> A stored state is trustworthy only while its timestamp is fresh.

The robot must publish `STOP` when a required sensor becomes stale, even when its old stored state says `PATH_CLEAR`.

---

## Original Safety Problems

I audited the current navigation logic instead of assuming that the reported problems definitely existed.

Two important safety weaknesses were found.

### Problem 1 — Early Return in the Freshness Function

The original freshness function contained a combined condition similar to:

```python
if self.last_camera_message_time is None or self.last_lidar_message_time is None:
    self.camera_fresh = False
    self.lidar_fresh = False
    self.decide_navigation()
    return
```

If the camera timestamp was `None`, the function also marked LiDAR as not fresh, even if LiDAR was publishing normally.

The early `return` also prevented the remaining sensor checks from running.

It could skip:

* independent LiDAR freshness calculation;
* left-sensor freshness calculation;
* right-sensor freshness calculation;
* freshness transition warnings.

This meant the navigation node did not always calculate a complete and accurate picture of all sensors.

### Problem 2 — Forward Movement Did Not Require All Sensors

The original main-package condition checked only camera and LiDAR freshness:

```python
if not self.camera_fresh or not self.lidar_fresh:
```

The robot could later publish:

```text
MOVE_FORWARD
```

when the front state was `PATH_CLEAR`, even if the left or right sensor was stale or unknown.

For a busy restaurant environment, I decided that all required sensors must be alive and trustworthy before any movement command is allowed.

---

## Independent Freshness Design

The safer freshness design checks every sensor independently.

Pseudocode:

```text
Get current time

IF camera timestamp is None:
    camera_fresh = False
ELSE:
    calculate camera message age
    convert the age into seconds
    compare the age with sensor_timeout

IF LiDAR timestamp is None:
    lidar_fresh = False
ELSE:
    calculate LiDAR message age
    convert the age into seconds
    compare the age with sensor_timeout

IF left timestamp is None:
    left_fresh = False
ELSE:
    calculate left message age
    convert the age into seconds
    compare the age with sensor_timeout

IF right timestamp is None:
    right_fresh = False
ELSE:
    calculate right message age
    convert the age into seconds
    compare the age with sensor_timeout

Update stale-sensor warning history

Call decide_navigation once
```

There is no early return inside the freshness calculation.

Every sensor receives its own accurate freshness value.

---

## Final Navigation Safety Checkpoints

The navigation node now uses safety checkpoints before normal navigation decisions.

A checkpoint is an `if` or `elif` condition that must be passed before movement is allowed.

### Freshness checkpoint

Conceptually:

```text
IF camera is not fresh
OR LiDAR is not fresh
OR left is not fresh
OR right is not fresh:
    STOP
```

The condition uses `or` because one unsafe sensor is enough to stop the robot.

For example:

```text
camera_fresh = True
lidar_fresh = True
left_fresh = False
right_fresh = True
```

Because `left_fresh` is false, the complete condition becomes true and the robot publishes `STOP`.

### Unknown-state checkpoint

The main navigation node combines camera and LiDAR into:

```text
front_state
```

The front-state rules are:

```text
Camera or LiDAR detects obstacle
    → front_state = OBSTACLE_DETECTED

Camera and LiDAR both report path clear
    → front_state = PATH_CLEAR

Any uncertain combination
    → front_state = UNKNOWN
```

The unknown-state checkpoint now protects:

```text
front_state
left_state
right_state
```

Conceptually:

```text
IF front_state is UNKNOWN
OR left_state is UNKNOWN
OR right_state is UNKNOWN:
    STOP
```

This means a message can be fresh but still unsafe.

Example:

```text
right_fresh = True
right_state = UNKNOWN
```

The freshness checkpoint passes because the message arrived recently.

The unknown-state checkpoint stops the robot because the message content is not usable for navigation.

---

## Final Decision Order

The navigation decision order is now:

```text
1. Update the combined front state.

2. If any required sensor is not fresh:
       STOP

3. Else if any required state is unknown:
       STOP

4. Else if the front has an obstacle:
       If the left side is clear:
           TURN_LEFT
       Else if the right side is clear:
           TURN_RIGHT
       Else:
           STOP

5. Else if the front path is clear:
       MOVE_FORWARD

6. Else:
       STOP
```

The safety checks happen before all movement decisions.

---

## State Versus Motor Command

I learned an important difference between a perception state and a motor command.

Sensor or navigation states describe what the robot knows:

```text
PATH_CLEAR
OBSTACLE_DETECTED
UNKNOWN
```

Motor commands describe what the robot should do:

```text
MOVE_FORWARD
TURN_LEFT
TURN_RIGHT
STOP
```

For example:

```text
front_state = UNKNOWN
```

does not mean that `front_state` becomes `STOP`.

Instead:

```text
front_state = UNKNOWN
        ↓
navigation decision
        ↓
motor command = STOP
```

The motor-control node then interprets `STOP` as:

```text
Both wheels stop safely
```

---

## Practice Workspace Testing

The practice package was rebuilt with:

```bash
cd /home/pradip/mission-korea-day20-practice/ros2_ws

python3 -m py_compile \
src/restaurant_robot_practice/restaurant_robot_practice/navigation_obstacle_subscriber.py

colcon build --packages-select restaurant_robot_practice

source install/setup.bash
```

The executable list was checked using:

```bash
ros2 pkg executables restaurant_robot_practice
```

The expected six executables were available.

---

## Practice Test Results

### Test 1 — Startup With No Sensor Messages

Only the navigation and motor-control nodes were started.

Expected freshness:

```text
camera_fresh = False
lidar_fresh = False
left_fresh = False
right_fresh = False
```

Result:

```text
motor command: STOP
```

Motor-control result:

```text
Both wheels stop safely
```

Test passed.

### Test 2 — Only Camera and LiDAR Running

Camera and LiDAR were publishing, but left and right had not published.

Expected:

```text
camera_fresh = True
lidar_fresh = True
left_fresh = False
right_fresh = False
```

Result:

```text
STOP
```

The robot did not move even when camera and LiDAR reported `PATH_CLEAR`.

Test passed.

### Test 3 — All Sensors Fresh

The left and right publishers were started.

Expected:

```text
camera_fresh = True
lidar_fresh = True
left_fresh = True
right_fresh = True
```

When the front path was clear, navigation published:

```text
MOVE_FORWARD
```

Motor control reported:

```text
Both wheels moving forward at the same speed
```

Test passed.

### Test 4 — One Sensor Becomes Stale

The left publisher was stopped.

Immediately after stopping, its latest message was still recent:

```text
left_fresh = True
```

After the timeout:

```text
left_fresh = False
```

The stored state still said:

```text
left_state = PATH_CLEAR
```

However, navigation published:

```text
STOP
```

Motor control reported:

```text
Both wheels stop safely
```

Test passed.

### Test 5 — Sensor Recovery

The left publisher was restarted.

A new message updated its timestamp.

Result:

```text
left_fresh = True
```

After every required sensor was fresh again, navigation resumed movement.

Test passed.

### Test 6 — Obstacle Present

The normal camera publisher was stopped, and a continuous manual obstacle message was published:

```bash
ros2 topic pub -r 1 \
/obstacle_status \
std_msgs/msg/String \
"{data: 'OBSTACLE_DETECTED'}"
```

With the left side fresh and clear, navigation published:

```text
TURN_LEFT
```

Motor control reported that the left wheel slowed and the right wheel moved faster.

The robot did not move straight into the obstacle.

Test passed.

### Fresh but `UNKNOWN` Test

A continuous fresh `UNKNOWN` message was published.

Example:

```bash
ros2 topic pub -r 1 \
/obstacle_status \
std_msgs/msg/String \
"{data: 'UNKNOWN'}"
```

The camera freshness became true because messages were arriving recently.

However:

```text
camera_state = UNKNOWN
```

The unknown-state checkpoint published:

```text
STOP
```

Test passed.

---

## Conflicting Publisher Discovery

During the obstacle test, the robot temporarily alternated between:

```text
MOVE_FORWARD
TURN_LEFT
```

The cause was two publishers sending different values to the same topic:

```text
normal camera publisher → PATH_CLEAR
manual publisher        → OBSTACLE_DETECTED
```

Every new message replaced the stored camera state.

The decision therefore changed repeatedly:

```text
PATH_CLEAR → MOVE_FORWARD
OBSTACLE_DETECTED → TURN_LEFT
```

I verified topic publishers using:

```bash
ros2 topic info /obstacle_status --verbose
```

This taught me that conflicting publishers on one sensor topic can produce unstable and unsafe decisions.

A controlled test should use only one source for each simulated sensor input.

---

## Main Package Changes

After the practice version passed, I repeated the improvement in:

```text
projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status/navigation_obstacle_subscriber.py
```

The meaningful changes were:

1. Camera, LiDAR, left, and right must all be fresh before movement.
2. Unknown left or right states now cause `STOP`.
3. Camera freshness is calculated independently.
4. LiDAR freshness is calculated independently.
5. A missing camera timestamp no longer automatically marks LiDAR stale.
6. The early return was removed.
7. Left and right freshness calculations can no longer be skipped.
8. The existing stale-transition warnings were preserved.
9. Existing `MOVE_FORWARD`, `TURN_LEFT`, and `TURN_RIGHT` behaviour was preserved.

---

## Main Package Build

The main package was checked and rebuilt:

```bash
cd ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws

python3 -m py_compile \
src/restaurant_robot_status/restaurant_robot_status/navigation_obstacle_subscriber.py

colcon build --packages-select restaurant_robot_status
```

Result:

```text
Build successful
```

---

## Main Package Test Results

### Main Test 1 — Startup

With no sensor publishers running:

```text
camera_fresh = False
lidar_fresh = False
left_fresh = False
right_fresh = False
```

Result:

```text
STOP
```

Motor control confirmed that both wheels stopped safely.

### Main Test 2 — Camera and LiDAR Only

Camera and LiDAR were running, while left and right remained unavailable.

The logs showed:

```text
Left: UNKNOWN
Left fresh: False
Right: UNKNOWN
Right fresh: False
Command: STOP
```

Even when:

```text
Front: PATH_CLEAR
```

the robot remained stopped.

### Main Test 3 — All Sensors Running

After starting left and right:

```text
Left fresh: True
Right fresh: True
```

When the front path was clear:

```text
Command: MOVE_FORWARD
```

When the front contained an obstacle and the left side was clear:

```text
Command: TURN_LEFT
```

Both normal movement and obstacle behaviour worked correctly.

### Main Test 4 — Left Sensor Stale

The left publisher was stopped.

After the configured timeout:

```text
Left: PATH_CLEAR
Left fresh: False
Command: STOP
```

This proved the robot did not trust the old `PATH_CLEAR` value.

### Main Test 5 — Left Sensor Recovery

The left publisher was restarted.

Result:

```text
Left fresh: True
```

Navigation resumed:

```text
Front clear → MOVE_FORWARD
Front obstacle → TURN_LEFT
```

### Main Test 6 — Fresh Right Sensor With `UNKNOWN`

The normal right publisher was stopped, and fresh `UNKNOWN` messages were published:

```bash
ros2 topic pub -r 1 \
/right_status \
std_msgs/msg/String \
"{data: 'UNKNOWN'}"
```

The logs showed:

```text
Right: UNKNOWN
Right fresh: True
Command: STOP
```

This proved that freshness alone is not enough.

The state must also be known.

---

## Integrated Launch Test

After individual testing, I stopped the manually started nodes and launched the complete system:

```bash
cd ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws
source install/setup.bash

ros2 launch restaurant_robot_status restaurant_robot_system.launch.py
```

All six nodes started successfully.

The logs showed:

```text
Left fresh: True
Right fresh: True
Front: OBSTACLE_DETECTED
Command: TURN_LEFT
```

Motor control correctly interpreted the command.

I also verified the runtime parameter:

```bash
ros2 param get /navigation_obstacle_subscriber sensor_timeout
```

Result:

```text
Double value is: 4.0
```

This confirmed that the launch system loaded the expected Day 24 configuration.

---

## Errors and Corrections

### Missing `not`

I initially wrote side-sensor freshness conditions without `not`.

Incorrect meaning:

```python
or self.left_fresh
```

This would stop the robot when the sensor was fresh.

Correct meaning:

```python
or not self.left_fresh
```

This stops the robot when the sensor is not fresh.

### Misspelled `self`

I wrote:

```python
slef.lidar_fresh
```

`py_compile` accepted the syntax, but it would fail at runtime because `slef` was not defined.

Correct:

```python
self.lidar_fresh
```

### Missing `self.`

I wrote variables such as:

```python
left_fresh
self_left_state
```

These are valid syntax but incorrect runtime names.

Correct node attributes are:

```python
self.left_fresh
self.left_state
```

### Incorrect Camera Variable

I wrote:

```python
camera-age.nanoseconds
```

Python would interpret this as subtraction.

Correct:

```python
camera_age.nanoseconds
```

### Comparing Incompatible Values

I initially compared:

```python
lidar_age <= self.sensor_timeout
```

`lidar_age` is a ROS duration object, while `sensor_timeout` is a number of seconds.

Correct:

```python
lidar_age_seconds <= self.sensor_timeout
```

### Wrong Function Placement

I temporarily placed camera-age calculation inside `decide_navigation()`.

This was incorrect because:

* `current_time` was created inside `check_sensor_freshness()`;
* freshness calculation belongs in the freshness function;
* navigation decisions and sensor-health calculations should have separate responsibilities.

### `py_compile` Limitation

I learned that:

```bash
python3 -m py_compile FILE
```

checks Python syntax but does not detect every runtime problem.

It did not detect:

```text
slef
self_left_state
missing self.
```

These names are syntactically valid but fail only when the code executes.

Therefore, syntax testing must be followed by runtime testing.

---

## Whitespace Check

I inspected the changes with:

```bash
git diff
git diff --stat
git diff --check
```

`git diff --check` initially found trailing whitespace.

I removed trailing spaces and checked again.

Final result:

```text
python3 -m py_compile → no output
git diff --check → no output
```

This means the Python syntax and Git whitespace checks passed.

---

## LiDAR Distance Measurement Discussion

Today’s main task was sensor freshness and unknown-state protection, but I also thought about future LiDAR development.

The responsibility should be divided as follows:

```text
LiDAR node
    measures obstacle distances
    publishes measurements

Navigation node
    interprets the measurements
    chooses STOP, TURN, or MOVE_FORWARD

Motor-control node
    executes the command
```

The LiDAR node should report facts.

The navigation node should make decisions.

A future beginner version could publish the nearest obstacle distance using:

```text
/lidar_distance
```

with:

```text
std_msgs/msg/Float32
```

Later, a more realistic ROS2 LiDAR system should use:

```text
sensor_msgs/msg/LaserScan
```

This would provide many range measurements across different angles.

The navigation node could then reason about:

```text
front-left distance
front distance
front-right distance
```

Possible future rules:

```text
Very close obstacle → emergency STOP

Obstacle inside navigation threshold:
    examine left and right space
    choose a safe turn

Safe forward distance:
    continue evaluating all required sensors
```

I did not add distance-based navigation today because it would mix a new topic with the Day 25 safety audit.

---

## Design Evolution

My original design was:

```text
If the front detects an obstacle:
    check left and right
    choose a turning direction
```

That design is still part of the navigation behaviour.

The new safety improvement adds another requirement:

> Even when the front looks clear, the robot should know that every required sensor is alive and trustworthy before it moves.

The robot does not necessarily use left and right states to choose every forward movement, but it verifies that the side-sensing system is healthy.

This is useful in a busy restaurant where people or objects may approach from the sides.

This design is conservative.

### Advantage

The robot stops safely when any required perception component becomes unavailable.

### Disadvantage

One failed side sensor can stop the complete robot even when the front appears clear.

In the future, I may research safe degraded operating modes. For now, stopping is the safer and easier behaviour to prove.

---

## Final Safety Test Summary

```text
No sensor messages
    → STOP

Only camera and LiDAR running
    → STOP

All sensors fresh and front clear
    → MOVE_FORWARD

Front obstacle and left clear
    → TURN_LEFT

One required sensor becomes stale
    → STOP

The failed sensor recovers
    → movement may resume

A sensor message is fresh but UNKNOWN
    → STOP
```

---

## What I Learned

I learned that safe robotics requires more than checking the latest stored sensor state.

The navigation node must know:

```text
What did the sensor report?
When did it report it?
Is the information still fresh?
Did every required sensor provide usable information?
```

I also learned:

* `None` means no timestamp has been received.
* A fresh message can still contain `UNKNOWN`.
* A known state can still be stale.
* Fresh does not automatically mean safe.
* Known does not automatically mean fresh.
* Movement requires both known and fresh information.
* An early `return` can accidentally skip important safety calculations.
* Every sensor should have its freshness calculated independently.
* A final safety checkpoint should run before navigation behaviour.
* One unsafe required sensor is enough to stop the robot.
* Measurement belongs in sensor nodes.
* Decision-making belongs in the navigation node.
* Motor execution belongs in the motor-control node.
* `py_compile` cannot detect every runtime naming mistake.
* Controlled ROS2 tests are necessary after syntax checks.

---

## Personal Reflection

Today I did more than change an `if` condition.

I audited the control flow of a multi-sensor navigation system and found how incomplete checks could allow unsafe movement.

At first, I knew that the robot should stop when information was missing, but I needed to understand exactly where that safety responsibility belonged.

I learned to separate:

```text
sensor-health calculation
navigation decision
motor execution
```

I also made several mistakes while constructing the code, including missing `not`, misspelling `self`, using the wrong variable type, and placing calculations in the wrong function.

Instead of copying a complete solution, I corrected each mistake in small steps and tested the result.

The most important lesson from Day 25 is:

> The robot must never move because an old value looks safe. It must move only when every required source of information is currently trustworthy.

---

## Final Status

Practice implementation:

```text
Completed and safety-tested
```

Main implementation:

```text
Completed and safety-tested
```

Main package build:

```text
Successful
```

Integrated launch:

```text
Successful
```

Runtime parameter:

```text
sensor_timeout = 4.0
```

Safety audit result:

```text
All required sensors must be fresh and known before movement.
```
