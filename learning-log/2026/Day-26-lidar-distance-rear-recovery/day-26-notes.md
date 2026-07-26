# Day 26 — LiDAR Distance, Rear Sensing and Safe Backward Recovery

## Today’s objective

Today I upgraded my ROS2 restaurant robot from using only symbolic obstacle states such as `PATH_CLEAR` to also using real numerical distance values.

I added:

* Front LiDAR distance measurement
* Distance freshness checking
* Distance validity checking
* A safety threshold for forward movement
* Rear obstacle status
* Rear distance measurement
* Rear-data freshness checking
* A new `MOVE_BACKWARD` motor command
* A guarded backward-recovery rule

All work was completed and tested inside the practice workspace:

```text
/home/pradip/mission-korea-day20-practice/ros2_ws
```

Package:

```text
restaurant_robot_practice
```

---

# 1. Why the robot needs numerical distance

Previously, the LiDAR publisher only sent:

```text
/lidar_status → PATH_CLEAR
```

This tells navigation that the path is clear, but it does not tell the robot how far away the obstacle is.

For example, both of these situations could incorrectly use the same status:

```text
Obstacle 3.0 metres away → PATH_CLEAR
Obstacle 0.6 metres away → PATH_CLEAR
```

The robot needs numerical distance to make safer decisions.

I added:

```text
/lidar_distance → std_msgs/msg/Float32
```

Example message:

```text
data: 3.0
```

This means the simulated front LiDAR detected the nearest obstacle at 3 metres.

---

# 2. Why two different ROS2 topics were used

The existing LiDAR topic uses:

```text
/lidar_status → std_msgs/msg/String
```

The new distance topic uses:

```text
/lidar_distance → std_msgs/msg/Float32
```

One ROS2 topic has one fixed message type. Therefore, one topic should not sometimes send:

```text
PATH_CLEAR
```

and sometimes send:

```text
3.0
```

The publisher and subscriber must always agree on the same message type.

The two LiDAR outputs are now:

```text
/lidar_status   → String  → PATH_CLEAR
/lidar_distance → Float32 → 3.0
```

---

# 3. Adding the front distance publisher

I imported both message types:

```python
from std_msgs.msg import String, Float32
```

The existing publisher remained responsible for `/lidar_status`.

A second publisher was created for `/lidar_distance`.

Important lesson:

Each publisher must have a separate Python variable.

Correct design:

```text
self.publisher          → /lidar_status
self.distance_publisher → /lidar_distance
```

At first, I used `self.publisher` for both publishers. The second assignment overwrote the reference to the first publisher.

`py_compile` accepted it because it was valid Python syntax, but it would have created a runtime message-type problem.

---

# 4. Simulated LiDAR distance

Because I do not currently have a physical LiDAR connected, I simulated a measurement:

```text
3.0 metres
```

A real physical LiDAR would calculate distance using reflected laser light. Its ROS2 driver would publish the measurements.

In my current simulation, I manually publish:

```text
/lidar_distance → 3.0
```

The LiDAR publisher now logs:

```text
lidar status: PATH_CLEAR
LiDAR distance: 3.0 metres
```

---

# 5. Verifying the new LiDAR topic

I checked the topic information:

```bash
ros2 topic info /lidar_distance
```

Result:

```text
Type: std_msgs/msg/Float32
Publisher count: 1
Subscription count: 0
```

When I ran:

```bash
ros2 topic echo /lidar_distance
```

the echo command temporarily became a subscriber.

The topic information then showed:

```text
Publisher count: 1
Subscription count: 1
```

This taught me that ROS2 command-line tools such as `ros2 topic echo` create temporary subscriber nodes.

---

# 6. Navigation subscription for distance

The navigation node now subscribes separately to:

```text
/lidar_status
/lidar_distance
```

Each subscription has:

```text
One message type
One topic
One callback
One queue size
```

I initially attempted to put two topics and two callbacks inside one `create_subscription()` call.

That does not work. Each topic requires a separate subscription object.

---

# 7. Front distance state variables

The navigation node now stores:

```text
self.lidar_distance
self.last_lidar_distance_time
self.lidar_distance_fresh
```

Initial values:

```text
lidar_distance = None
last_lidar_distance_time = None
lidar_distance_fresh = False
```

`None` means:

```text
No numerical distance message has been received yet.
```

`None` is safer than starting with `0.0`.

A value of `0.0` could mean a real obstacle is touching the sensor, while `None` clearly means that no measurement exists yet.

---

# 8. Front distance callback

The distance callback performs three jobs:

```text
1. Store the latest distance
2. Record the message arrival time
3. Recalculate navigation
```

Conceptually:

```text
Receive Float32 message
Store message.data
Record current ROS2 time
Call decide_navigation()
```

---

# 9. Distance freshness

A recent safe value must not be trusted forever.

Example:

```text
Stored distance = 3.0 metres
Distance publisher stops
```

The stored number still says `3.0`, but it becomes outdated.

The freshness checker calculates:

```text
distance age = current time - last message time
```

Then:

```text
age <= sensor_timeout → fresh
age > sensor_timeout  → stale
```

The current parameter is:

```text
sensor_timeout = 3.0 seconds
```

The navigation safety gate now checks:

```text
Camera freshness
LiDAR status freshness
LiDAR distance freshness
Left freshness
Right freshness
Rear status freshness
Rear distance freshness
```

If any required input is stale:

```text
STOP
```

---

# 10. Front distance safety threshold

I selected an initial front safety threshold:

```text
1.0 metre
```

Current rule:

```text
distance > 1.0 metre  → forward movement may be allowed
distance <= 1.0 metre → unsafe
```

Boundary results:

```text
3.0 m → safe enough for forward movement
1.2 m → safe enough for forward movement
1.0 m → unsafe
0.6 m → unsafe
```

Using:

```python
distance > 1.0
```

means exactly `1.0` is not considered safe enough.

---

# 11. Navigation safety order

The navigation node checks the most dangerous conditions first.

Current decision order:

```text
1. Any required data stale
   → STOP

2. Any required state unknown or distance missing
   → STOP

3. Front or rear distance invalid
   → STOP

4. Front obstacle dangerously close
   → consider guarded backward recovery

5. Camera and LiDAR clear, front distance safe
   → MOVE_FORWARD

6. Left side clear
   → TURN_LEFT

7. Right side clear
   → TURN_RIGHT

8. No safe option
   → STOP
```

The order matters because a safety condition must return before movement logic is allowed to continue.

---

# 12. Invalid distance protection

A sensor can produce invalid measurements such as:

```text
NaN
Infinity
Negative values
Zero
```

I imported:

```python
import math
```

The robot now rejects distances that are:

```text
Not finite
Less than or equal to zero
```

`math.isfinite()` rejects:

```text
NaN
Positive infinity
Negative infinity
```

The numerical checks reject:

```text
0.0
Negative distances
```

Important lesson:

A negative distance already satisfies `distance <= 1.0`, but stopping because of the normal threshold is not the same as explicitly recognising invalid sensor data.

Safe robotics code should clearly separate:

```text
Missing data
Invalid data
Stale data
Valid but dangerous data
Valid and safe data
```

---

# 13. Runtime tests for front distance

## Test 1 — Missing sensors

Running only navigation and the LiDAR publisher produced:

```text
STOP
```

Reason:

```text
Camera, left and right data were missing and not fresh.
```

Result:

```text
PASS
```

## Test 2 — All inputs fresh

With camera, LiDAR status, LiDAR distance, left and right publishers running:

```text
Camera = PATH_CLEAR
LiDAR status = PATH_CLEAR
LiDAR distance = 3.0
Left = PATH_CLEAR
Right = PATH_CLEAR
```

Result:

```text
MOVE_FORWARD
```

Result:

```text
PASS
```

## Test 3 — Distance becomes stale

I stopped `/lidar_distance` but kept `/lidar_status` publishing.

The robot initially continued using the recent distance, but after the timeout:

```text
MOVE_FORWARD → STOP
```

This proved that an old safe-looking distance is not trusted forever.

Result:

```text
PASS
```

## Test 4 — Distance 0.6 metres

With all states fresh and `/lidar_status` still saying `PATH_CLEAR`:

```text
/lidar_distance = 0.6
```

Result:

```text
STOP
```

The numerical distance had higher safety priority than the symbolic `PATH_CLEAR` status.

Result:

```text
PASS
```

## Test 5 — Exact boundary

Distance:

```text
1.0 metre
```

Result:

```text
STOP
```

Because:

```text
1.0 <= 1.0
```

Result:

```text
PASS
```

## Test 6 — Recovery above threshold

Distance:

```text
1.2 metres
```

With every other input fresh and clear:

```text
MOVE_FORWARD
```

Result:

```text
PASS
```

---

# 14. Why the robot needs rear sensing

The original robot could only:

```text
MOVE_FORWARD
TURN_LEFT
TURN_RIGHT
STOP
```

It could not move backward.

A robot may need to reverse when:

```text
It enters a dead end
The front becomes blocked
There is not enough room for a U-turn
Turning left and right are both unsafe
It needs to reposition before turning
```

A U-turn is not always appropriate because:

```text
The corridor may be narrow
A wall may block rotation
A person may be nearby
The robot may not have enough turning space
```

However, the robot must not reverse blindly.

Front safety does not prove that the space behind the robot is safe.

Therefore, I added rear perception before adding automatic backward movement.

---

# 15. Rear publisher node

New file:

```text
rear_obstacle_publisher.py
```

The rear publisher sends:

```text
/rear_status   → std_msgs/msg/String
/rear_distance → std_msgs/msg/Float32
```

Current simulated values:

```text
rear status = PATH_CLEAR
rear distance = 3.0 metres
```

Both messages are published once per second from one timer callback.

The node logs:

```text
rear status: PATH_CLEAR
rear distance: 3.0
```

---

# 16. Registering the rear publisher

The node was added to `setup.py`:

```text
rear_obstacle_publisher =
restaurant_robot_practice.rear_obstacle_publisher:main
```

I initially used the incorrect spelling:

```text
rare_obstacle_publisher
```

This was fixed to:

```text
rear_obstacle_publisher
```

The package was rebuilt, and the node ran successfully.

---

# 17. Rear navigation state

The navigation node now stores:

```text
rear_state
last_rear_message_time
rear_fresh
```

and:

```text
rear_distance
last_rear_distance_message_time
rear_distance_fresh
```

Initial values:

```text
rear_state = UNKNOWN
rear_distance = None
rear_fresh = False
rear_distance_fresh = False
```

I initially accidentally wrote:

```text
rear_distance = False
```

This would overwrite the numerical distance variable with a Boolean.

It was corrected by using two separate variables:

```text
rear_distance       → numerical value
rear_distance_fresh → Boolean freshness status
```

---

# 18. Rear subscriptions and callbacks

The navigation node subscribes separately to:

```text
/rear_status
/rear_distance
```

Callbacks:

```text
receive_rear()
receive_rear_distance()
```

The status callback stores:

```text
rear_state
rear message time
```

The distance callback stores:

```text
rear_distance
rear-distance message time
```

Both callbacks call:

```text
decide_navigation()
```

I learned that callback and subscription names must match exactly.

Errors such as:

```text
recive_rear
receive_rear
receive_rear_distance
```

can be valid Python syntax but fail when ROS2 tries to find the callback.

---

# 19. Rear freshness

Rear status and rear distance have independent freshness checks.

This is necessary because one rear topic could continue publishing while the other stops.

The robot should not reverse unless both are recent.

The freshness variables are:

```text
rear_fresh
rear_distance_fresh
```

The navigation node stops when either rear stream becomes stale.

---

# 20. Directional safety

An important design correction was made.

At first, I added a global rule:

```text
If rear distance <= 1.0 metre:
    STOP
```

This was too broad.

Example:

```text
Front = clear
Rear obstacle = 0.5 metre behind
```

Moving forward could increase the distance from the rear obstacle.

Therefore:

```text
Front distance should protect forward movement.
Rear distance should protect backward movement.
```

A close rear obstacle should not automatically block safe forward movement.

The global rear-distance stop rule was removed.

---

# 21. MOVE_BACKWARD motor command

The motor-control subscriber now recognises:

```text
MOVE_BACKWARD
```

Its simulated motor behaviour is:

```text
Both wheels moving backward at the same speed
```

I directly tested the command:

```text
/motor_command → MOVE_BACKWARD
```

Motor output:

```text
Both wheels moving backward at the same speed
```

Result:

```text
PASS
```

---

# 22. Guarded backward recovery

The robot now has an initial guarded recovery rule.

Conceptually:

```text
If the front distance is <= 1.0 metre:

    If rear status is PATH_CLEAR
    AND rear distance is greater than 1.0 metre:
        MOVE_BACKWARD

    Otherwise:
        STOP
```

This means the robot reverses only when:

```text
Front is dangerously close
Rear status is clear
Rear distance is valid
Rear distance is fresh
Rear distance is greater than 1.0 metre
All other required sensor data is fresh and known
```

If rear data is missing, stale, invalid or blocked:

```text
STOP
```

---

# 23. Backward recovery runtime test

Test situation:

```text
Front distance = 0.6 metres
Rear status = PATH_CLEAR
Rear distance = 3.0 metres
All required sensor data fresh and valid
```

Expected:

```text
MOVE_BACKWARD
```

The complete runtime test passed.

Result:

```text
PASS
```

---

# 24. Important errors and lessons

## Error: Reusing the same publisher variable

Problem:

```text
Second publisher overwrote the first publisher reference.
```

Lesson:

```text
Every publisher should have its own clear variable.
```

## Error: Combining two topics into one subscription

Problem:

```text
One create_subscription call was given two topics and callbacks.
```

Lesson:

```text
One subscription handles one message type, one topic and one callback.
```

## Error: `retrun`

I accidentally wrote:

```text
retrun
```

`py_compile` accepted it because Python treated it as a normal variable name.

At runtime, it would produce:

```text
NameError
```

Lesson:

```text
py_compile checks syntax but does not prove that every name is correct.
```

## Error: Wrong class name

The class was:

```text
RearObstaclePublisher
```

but `main()` initially tried to create:

```text
RareObstaclePublisher
```

This would fail at runtime.

## Error: `rare` versus `rear`

Many rear variables initially used inconsistent spellings.

I used `grep` to find them:

```bash
grep -n "rare" navigation_obstacle_subscriber.py
```

Lesson:

```text
Consistent naming is critical in systems with many related state variables.
```

## Error: Timestamp mismatch

The rear-distance callback updated:

```text
last_rear_distance_message_time
```

but the freshness checker initially read a different name.

The names were made consistent.

## Error: Missing comma

A missing comma between a callback and queue size caused an invalid subscription structure.

## Error: Creating messages without publishing them

Creating:

```text
message = String()
distance_message = Float32()
```

does not send anything.

The publisher must explicitly call:

```text
publisher.publish(message)
```

---

# 25. What I understand now

I now understand that robotic safety is not based only on the latest sensor value.

A navigation system must check:

```text
Did the message arrive?
Is it fresh?
Is its type correct?
Is the value finite?
Is the value physically valid?
Is it above or below the directional threshold?
Is the intended movement direction safe?
```

I also understand that safety is directional:

```text
Front sensors protect forward movement.
Rear sensors protect backward movement.
Side sensors protect turning decisions.
```

A single global obstacle rule is not enough for a robot that can move in multiple directions.

---

# 26. Current robot inputs

The navigation node now receives:

```text
Camera status
Front LiDAR status
Front LiDAR distance
Left status
Right status
Rear status
Rear distance
```

Topics:

```text
/obstacle_status
/lidar_status
/lidar_distance
/left_status
/right_status
/rear_status
/rear_distance
```

Output:

```text
/motor_command
```

Possible commands:

```text
MOVE_FORWARD
MOVE_BACKWARD
TURN_LEFT
TURN_RIGHT
STOP
STOP_AND_WAIT
```

---

# 27. Current limitations

The current backward recovery rule is only an initial version.

The robot may repeatedly switch between:

```text
MOVE_FORWARD
MOVE_BACKWARD
MOVE_FORWARD
MOVE_BACKWARD
```

if the front measurement repeatedly crosses the threshold.

This is called oscillation.

The robot also does not yet control:

```text
How long it moves backward
How far it reverses
When recovery is complete
Whether it should turn after reversing
Whether enough turning space exists
```

A real recovery behaviour should use a state machine such as:

```text
NORMAL_NAVIGATION
STOPPED_BY_FRONT_OBSTACLE
REVERSING
CHECKING_TURN_SPACE
TURNING
RECOVERY_COMPLETE
```

---

# 28. Possible next improvements

Future work can include:

```text
Separate front and rear safety thresholds
Configurable distance parameters
Backward movement time limit
Recovery state machine
Hysteresis to prevent oscillation
Rear obstacle status derived from rear distance
Different speed commands
SLOW_FORWARD
SLOW_BACKWARD
Emergency-stop distance
Warning-distance zone
Turning-space validation
Launch-file integration
Main-project migration after practice verification
```

Example distance zones:

```text
Distance > 1.5 m       → normal movement
Distance 1.0–1.5 m     → slow movement
Distance 0.5–1.0 m     → stop or recovery
Distance <= 0.5 m      → emergency stop
```

The current robot does not yet support speed control, so it currently uses only full movement or stop commands.

---

# 29. Final result

Today I changed the robot from a simple state-based system into a more realistic distance-aware and direction-aware navigation system.

The robot can now:

```text
Receive numerical front distance
Reject stale front distance
Reject invalid front distance
Stop at the front safety threshold
Receive rear status and distance
Reject stale rear data
Reject invalid rear distance
Understand MOVE_BACKWARD
Reverse only when the front is blocked and the rear is safe
```

All planned practice tests were completed successfully.

---

# Personal reflection

Today I did more than add another ROS2 publisher.

I learned how safety grows as robot movement becomes more capable.

When the robot could only move forward, front sensing was enough for a basic demonstration. Once I wanted the robot to move backward, I had to add rear perception, separate freshness tracking, value validation and directional safety rules.

Every new robot capability creates new risks that must be handled deliberately.

I also learned that successful compilation does not guarantee correct behaviour. Naming errors, overwritten variables, wrong callbacks and incorrect decision order can survive syntax checking and appear only during runtime.

I am now beginning to think less like someone who only writes code and more like someone who designs a safe robotic system.
