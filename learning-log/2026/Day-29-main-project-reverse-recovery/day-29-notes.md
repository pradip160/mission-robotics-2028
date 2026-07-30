# Day 29 — Main ROS2 Project: Safe Reverse Recovery Completed

## Objective

Today I completed the safe reverse-recovery system in the main restaurant delivery robot project.

The robot can now:

* Detect when a front obstacle is dangerously close.
* Check whether the rear path is safe.
* Enter a reverse-recovery state.
* Continue reversing until enough front clearance exists.
* Stop reversing immediately if the rear becomes unsafe.
* Prevent rapid switching between forward and backward movement.

---

## Workspace

Main repository:

```text
~/mission-korea
```

ROS2 workspace:

```text
~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws
```

ROS2 package:

```text
restaurant_robot_status
```

Main navigation file:

```text
src/restaurant_robot_status/restaurant_robot_status/navigation_obstacle_subscriber.py
```

---

## 1. Completed Rear-Distance Freshness

The rear-distance callback already stored:

```text
rear_distance
last_rear_distance_message_time
```

Today I completed its freshness calculation.

Logic:

```text
If no rear-distance message has arrived:
    rear_distance_fresh = False

Otherwise:
    calculate the message age
    convert nanoseconds into seconds
    compare the age with sensor_timeout
```

The navigation safety gate now checks:

```text
camera freshness
LiDAR-status freshness
LiDAR-distance freshness
rear-status freshness
rear-distance freshness
left-sensor freshness
right-sensor freshness
```

If any required message is stale or missing:

```text
STOP
```

---

## 2. Added Numerical-Distance Validation

I imported Python’s `math` module and added checks for invalid front and rear distances.

The navigation node stops when either distance is:

```text
NaN
positive infinity
negative infinity
zero
negative
```

The validation logic uses:

```python
math.isfinite()
```

This prevents invalid sensor measurements from being treated as safe physical distances.

---

## 3. Confirmed MOVE_BACKWARD Support

The motor-control node already contained support for:

```text
MOVE_BACKWARD
```

Its motor interpretation is:

```text
Both wheels move backward
```

I confirmed the motor-control file compiled successfully.

---

## 4. Added Recovery-State Variables

The navigation node now stores:

```text
recovery_state = NORMAL
recovery_clear_distance = 1.5
```

Possible recovery state used today:

```text
NORMAL
REVERSING
```

`NORMAL` means the robot is using ordinary navigation logic.

`REVERSING` means the robot is currently performing obstacle recovery.

---

## 5. Reverse-Start Threshold

Reverse recovery starts when:

```text
front LiDAR distance <= 1.0 metre
```

However, the robot does not reverse automatically based only on the front obstacle.

It first verifies:

```text
rear_state == PATH_CLEAR
rear_distance > 1.0 metre
```

When both rear conditions are safe:

```text
recovery_state = REVERSING
motor command = MOVE_BACKWARD
```

When the rear is unsafe:

```text
motor command = STOP
```

This creates guarded reverse movement instead of blind reverse movement.

---

## 6. REVERSING-State Behaviour

While the robot is in the `REVERSING` state, the navigation node first checks the rear.

### Rear becomes unsafe

If:

```text
rear_state is not PATH_CLEAR
```

or:

```text
rear_distance <= 1.0 metre
```

the robot commands:

```text
STOP
```

The recovery state remains `REVERSING`.

This allows recovery to resume later if the rear becomes safe again.

### Front becomes sufficiently clear

If:

```text
lidar_distance >= 1.5 metres
```

the robot:

```text
changes recovery_state to NORMAL
commands STOP
```

The `STOP` creates a safe transition between reversing and normal movement.

On a later sensor callback, normal navigation can evaluate whether moving forward is safe.

### Recovery remains incomplete

When:

```text
rear remains safe
front distance is below 1.5 metres
```

the robot continues:

```text
MOVE_BACKWARD
```

---

## 7. Hysteresis

The system uses two different distance thresholds:

```text
Start reversing: front distance <= 1.0 metre
Finish reversing: front distance >= 1.5 metres
```

The difference is:

```text
0.5 metres
```

This gap is called hysteresis.

Without hysteresis, small sensor noise around one threshold could cause:

```text
MOVE_BACKWARD
MOVE_FORWARD
MOVE_BACKWARD
MOVE_FORWARD
```

That would make the robot shake or oscillate.

With hysteresis:

```text
0.9 metres → start reversing
1.1 metres → continue reversing
1.3 metres → continue reversing
1.5 metres → stop recovery and return to NORMAL
```

---

## 8. Final Navigation Decision Order

The main navigation decision order is now:

```text
1. Update fused front state.

2. If any required sensor is stale:
       STOP

3. If either numerical distance is invalid:
       STOP

4. If any required symbolic state is UNKNOWN:
       STOP

5. If recovery_state is REVERSING:
       check rear safety
       check front recovery clearance
       otherwise continue MOVE_BACKWARD

6. If front distance <= 1.0 metre:
       enter REVERSING only when rear is safe
       otherwise STOP

7. If front symbolic state reports an obstacle:
       TURN_LEFT when left is clear
       otherwise TURN_RIGHT when right is clear
       otherwise STOP

8. If front symbolic state is PATH_CLEAR:
       MOVE_FORWARD

9. Otherwise:
       STOP
```

This order is important because safety and recovery must be processed before normal forward or turning decisions.

---

## 9. Rear Publisher

The main package now contains:

```text
rear_obstacle_publisher.py
```

It publishes:

```text
/rear_status
/rear_distance
```

Current simulated safe rear values:

```text
rear_status = PATH_CLEAR
rear_distance = 3.0 metres
```

The executable is registered in `setup.py` as:

```text
rear_obstacle_publisher
```

---

## 10. Main LiDAR Publisher

The main LiDAR publisher now publishes both:

```text
/lidar_status
/lidar_distance
```

Consistent simulated pairs:

```text
PATH_CLEAR → 3.0 metres
OBSTACLE_DETECTED → 0.6 metres
```

The symbolic status and numerical distance are published from the same callback so they describe the same simulated sensor observation.

---

## 11. Runtime Verification

The package built successfully:

```text
Summary: 1 package finished
```

The updated navigation node started without runtime errors.

The reverse-recovery tests were completed successfully.

Verified behaviours included:

```text
Front dangerously close and rear safe
→ MOVE_BACKWARD

Robot already REVERSING and front not yet clear
→ continue MOVE_BACKWARD

Front reaches recovery-clear threshold
→ STOP
→ state changes to NORMAL

Rear becomes unsafe during recovery
→ STOP

Required sensor data missing or stale
→ STOP

Invalid numerical distance
→ STOP
```

---

## 12. Git Quality Check

I ran:

```bash
git diff --check
```

Git initially found trailing whitespace in:

```text
motor_control_subscriber.py
navigation_obstacle_subscriber.py
```

I removed only the invisible trailing spaces at the ends of lines.

I ran `git diff --check` again.

Final result:

```text
No output
```

This means the whitespace check passed.

---

## 13. Files Changed

Modified:

```text
lidar_obstacle_publisher.py
motor_control_subscriber.py
navigation_obstacle_subscriber.py
setup.py
```

Created:

```text
rear_obstacle_publisher.py
```

The main implementation now includes front numerical distance, rear sensing and state-based reverse recovery.

---

## Important Mistakes and Lessons

### Comparisons must be inside a condition

Writing:

```python
self.rear_state != 'PATH_CLEAR'
self.rear_distance <= 1.0
```

does not control behaviour by itself.

The comparisons must be part of an `if` condition.

### Multiple conditions need a logical operator

Two safety conditions must be connected using:

```text
or
```

when either danger should stop the robot.

Rear safety before reversing uses:

```text
and
```

because both rear conditions must be safe.

### Assignment and comparison are different

Changing the state requires assignment:

```text
recovery_state = REVERSING
```

Checking the state requires comparison:

```text
recovery_state == REVERSING
```

### Decision order matters

The `REVERSING` branch must appear before ordinary forward and turning logic.

Otherwise, normal navigation could publish another motor command before recovery is handled.

### Compilation does not prove logical correctness

`py_compile` confirms valid Python syntax.

It does not prove that:

```text
the correct variable was changed
the conditions are in the correct order
ROS2 message types match
the recovery behaviour is safe
```

Therefore the complete workflow remains:

```text
Inspect code
Run py_compile
Build with colcon
Restart nodes
Perform controlled ROS2 topic tests
Inspect Git changes
Run git diff --check
```

---

## What I Learned

Today I learned how a robot can remember an ongoing safety behaviour.

The robot does not make every decision as though nothing happened before.

The `recovery_state` gives it memory:

```text
I was blocked.
I started reversing.
I must continue recovery until the front is sufficiently clear.
```

This is a basic state-machine concept.

I also learned why real robot recovery requires:

```text
front sensing
rear sensing
sensor freshness
numerical validation
safe thresholds
state memory
hysteresis
careful decision priority
```

A simple `if obstacle: move backward` rule would not be safe enough.

---

## Current Capability

The main restaurant delivery robot can now:

```text
Combine camera and LiDAR symbolic states
Use numerical front distance
Use rear status and numerical distance
Detect stale sensor information
Reject invalid distances
Stop when information is uncertain
Turn toward a clear side
Move forward when the front is safe
Reverse only when the rear is safe
Remember that recovery is active
Continue recovery through the hysteresis region
Stop when recovery is complete
Stop immediately if the rear becomes unsafe
```

This is an important improvement from reactive obstacle avoidance toward a state-based robot safety controller.

---

## Next Development Step

The next safety limitation is unlimited recovery duration.

If the front never reaches `1.5 metres`, the robot could continue attempting reverse recovery for too long while the rear remains clear.

A future improvement should add:

```text
maximum reverse duration
maximum recovery attempts
recovery failure state
STOP_AND_WAIT or human assistance request
recovery-state logging
```

This would prevent endless reverse recovery and make the controller more robust.
