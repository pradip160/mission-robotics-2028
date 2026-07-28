# Day 28 — Main ROS2 Project: LiDAR Distance and Rear Sensor Migration

## Objective

Today I began transferring the tested distance-based safety and rear-recovery infrastructure from my practice workspace into the main restaurant delivery robot project.

The work was completed slowly and incrementally. After every small edit, I used `py_compile`, rebuilt the ROS2 package when necessary, and performed runtime topic tests.

---

## Main Workspace

```text
~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws
```

Main package:

```text
restaurant_robot_status
```

---

## 1. Added Numerical LiDAR Distance Publishing

The existing LiDAR publisher originally published only a symbolic status:

```text
/lidar_status
```

Possible values:

```text
PATH_CLEAR
OBSTACLE_DETECTED
```

I imported:

```python
Float32
```

I then created a second publisher:

```text
/lidar_distance
```

The LiDAR node now publishes consistent status and distance pairs from the same timer callback:

```text
PATH_CLEAR          → 3.0 metres
OBSTACLE_DETECTED   → 0.6 metres
```

Publishing both values from the same callback reduces the risk of status and distance becoming inconsistent.

### Important bug fixed

I initially wrote:

```python
self.distance_publisher.publish(message)
```

This attempted to publish a `String` message through a `Float32` publisher.

I corrected it so the distance publisher sends the numerical message.

I also restored the status toggle:

```text
PATH_CLEAR → OBSTACLE_DETECTED → PATH_CLEAR
```

---

## 2. LiDAR Runtime Test

I compiled and built the package successfully.

The LiDAR publisher produced alternating output:

```text
Lidar_obstacle: PATH_CLEAR
lidar distance: 3.0

Lidar_obstacle: OBSTACLE_DETECTED
lidar distance: 0.6
```

I confirmed that another ROS2 process could receive the distance topic:

```bash
ros2 topic echo /lidar_distance --once
```

Received:

```text
data: 0.6000000238418579
```

This is normal `Float32` precision and represents approximately `0.6 metres`.

---

## 3. Connected LiDAR Distance to Navigation

Inside `navigation_obstacle_subscriber.py`, I added storage for:

```text
lidar_distance
last_lidar_distance_message_time
lidar_distance_fresh
```

I created:

```text
receive_lidar_distance()
```

Its responsibilities are:

1. Store the newest numerical distance.
2. Record the ROS arrival time.
3. Re-run the navigation decision.

I also added a new subscription:

```text
/lidar_distance
std_msgs/msg/Float32
```

The installed navigation node confirmed the subscription:

```text
/lidar_distance: std_msgs/msg/Float32
```

---

## 4. Added LiDAR-Distance Freshness Safety

The navigation node now checks the age of the numerical LiDAR message.

Logic:

```text
No distance message received
→ lidar_distance_fresh = False

Recent distance message
→ lidar_distance_fresh = True

Distance message older than sensor_timeout
→ lidar_distance_fresh = False
```

The main stale-sensor safety condition now includes:

```text
camera status
LiDAR status
LiDAR distance
left status
right status
rear status
```

If a required input is missing or stale, the command is:

```text
STOP
```

---

## 5. Added Front Distance Safety Rule

I kept the existing `update_front_state()` function unchanged.

It still performs symbolic camera and LiDAR fusion:

```text
Camera obstacle OR LiDAR obstacle
→ front_state = OBSTACLE_DETECTED

Camera clear AND LiDAR clear
→ front_state = PATH_CLEAR

Otherwise
→ front_state = UNKNOWN
```

The numerical distance is checked separately.

Temporary front safety rule:

```text
LiDAR distance <= 1.0 metre
→ STOP
```

This rule will later become guarded reverse recovery after the rear system is fully connected.

---

## 6. Controlled Front-Distance Runtime Tests

For testing, I continuously published fresh sensor messages using:

```bash
ros2 topic pub --rate 1
```

I learned that:

```text
--rate 1  → one message every second
--rate 2  → two messages every second
--once    → publish one message and stop
```

Continuous publishing was necessary because the navigation system has a three-second sensor timeout.

### Unsafe-distance test

Inputs:

```text
Camera status = PATH_CLEAR
LiDAR status = PATH_CLEAR
Left status = PATH_CLEAR
Right status = PATH_CLEAR
LiDAR distance = 0.6 metres
```

Result:

```text
STOP
```

This proved that numerical distance has priority over a conflicting symbolic `PATH_CLEAR` status.

### Safe-distance test

Inputs:

```text
All status topics = PATH_CLEAR
LiDAR distance = 3.0 metres
```

Result:

```text
MOVE_FORWARD
```

Therefore:

```text
0.6 metres → STOP
3.0 metres → MOVE_FORWARD
```

The front numerical-distance migration was successfully tested.

---

## 7. Created the Rear Sensor Publisher

I copied the LiDAR publisher structure to create:

```text
rear_obstacle_publisher.py
```

I renamed:

```text
Class: RearObstaclePublisher
Node: rear_obstacle_publisher
Callback: publish_rear_status
```

The rear node publishes:

```text
/rear_status
/rear_distance
```

Message types:

```text
/rear_status   → std_msgs/msg/String
/rear_distance → std_msgs/msg/Float32
```

For the current recovery test, the rear sensor remains continuously clear:

```text
rear_status = PATH_CLEAR
rear_distance = 3.0 metres
```

I removed the alternating obstacle toggle from the rear publisher.

---

## 8. Registered the Rear Executable

I added the rear publisher to `setup.py`.

I also found and removed an invalid old executable entry that referenced a nonexistent file and contained an incorrect space before `main`.

The new executable was successfully registered:

```text
restaurant_robot_status rear_obstacle_publisher
```

---

## 9. Rear Publisher Runtime Test

I ran:

```bash
ros2 run restaurant_robot_status rear_obstacle_publisher
```

The node continuously published clear rear information.

I confirmed the distance topic:

```bash
ros2 topic echo /rear_distance --once
```

Result:

```text
data: 3.0
```

---

## 10. Connected Rear Status to Navigation

I added rear-status state variables:

```text
rear_state
last_rear_message_time
rear_fresh
previous_rear_fresh
```

I created:

```text
receive_rear()
```

Responsibilities:

1. Store `/rear_status`.
2. Record its arrival time.
3. Re-run navigation.

I added the `/rear_status` subscription.

I also added rear-status freshness logic.

The navigation node now stops when:

```text
Rear status is missing
Rear status is stale
Rear state is UNKNOWN
```

---

## 11. Began Connecting Rear Distance

I added rear-distance variables:

```text
rear_distance = 0.0
last_rear_distance_message_time = None
rear_distance_fresh = False
```

I created:

```text
receive_rear_distance()
```

Responsibilities:

1. Store the newest rear numerical distance.
2. Record its arrival time.
3. Re-run navigation.

I added the subscription:

```text
/rear_distance
std_msgs/msg/Float32
```

The navigation file compiled successfully after these changes.

---

## Mistakes and Lessons

### Nano warning screen

Nano appeared blank because it was warning that the file might already be open in another editing session.

Pressing `Y` opened the real existing file.

The file was not empty.

### Assignment names must remain consistent

Examples of errors found and corrected:

```text
lasr → last
rare → rear
rear_freshness → rear_fresh
sesnsor_timeout → sensor_timeout
Fasle → False
```

### A method and variable should not share the same name

I initially attempted to name the rear-distance callback:

```text
rear_distance
```

But `self.rear_distance` was already a variable.

I changed the method name to:

```text
receive_rear_distance
```

### `py_compile` has limits

`py_compile` catches syntax and indentation errors.

It does not always detect:

```text
Misspelled runtime variable names
Incorrect logical assignments
Wrong ROS2 message types
Wrong publisher-message combinations
Missing required behaviour
```

Therefore I must combine:

```text
Code inspection
py_compile
colcon build
ROS2 runtime tests
```

---

## Current System State

Completed in the main project:

```text
LiDAR status publisher
LiDAR numerical-distance publisher
LiDAR-distance navigation subscription
LiDAR-distance freshness
Front <= 1.0 metre STOP rule
Front safe/unsafe runtime tests
Rear status and distance publisher
Rear executable registration
Rear publisher runtime test
Rear-status navigation subscription
Rear-status freshness and UNKNOWN safety
Rear-distance storage
Rear-distance callback
Rear-distance subscription
```

Not yet completed:

```text
Rear-distance freshness logic
Rear-distance stale safety check
Invalid distance checks for NaN, infinity and non-positive values
MOVE_BACKWARD motor support in the main project
NORMAL and REVERSING recovery states
1.0 metre reverse-start threshold
1.5 metre recovery-clear threshold
Full reverse-recovery runtime tests
Final build, notes review, commit and push
```

---

## Tomorrow’s Exact Starting Point

Continue inside:

```text
navigation_obstacle_subscriber.py
```

First task:

Add rear-distance freshness logic inside `check_sensor_freshness()`.

Required logic:

```text
If no rear-distance message has arrived:
    rear_distance_fresh = False

Otherwise:
    calculate rear-distance message age
    convert nanoseconds to seconds
    compare with sensor_timeout
```

After that:

```text
Add rear_distance_fresh to the stale safety gate
Add finite and positive distance validation
Add MOVE_BACKWARD support
Add NORMAL and REVERSING recovery state
Test guarded reverse and hysteresis
```

---

## Reflection

Today I did not blindly copy the practice project into the main project.

I inspected the existing architecture and migrated each feature gradually. I made several mistakes, but I identified and corrected them through careful naming checks, compilation, builds and runtime tests.

The main robot now understands not only whether the front path is symbolically clear, but also the numerical distance in front. It also has working rear sensor topics and most of the navigation infrastructure required for safe reverse recovery.
