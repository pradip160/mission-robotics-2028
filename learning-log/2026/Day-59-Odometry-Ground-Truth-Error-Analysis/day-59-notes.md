# Day 59 – Odometry Ground Truth and Error Analysis

Date: 19 September 2026

## Goal

Begin moving from:

```text
"I implemented odometry."
```

toward:

```text
"How accurate is my odometry?"
```

The goal is to compare my custom wheel odometry against an independent Gazebo ground-truth pose and measure odometry error.

---

## 1. What We Are Comparing

There are now two different sources of robot pose.

### Custom Wheel Odometry

My custom odometry estimates robot motion from wheel rotation:

```text
wheel rotation
      ↓
wheel displacement
      ↓
delta_s / delta_theta
      ↓
x / y / theta
      ↓
/odom
```

This is an **estimate**.

### Gazebo Ground Truth

Gazebo runs the simulation physics and knows the simulated position of the robot model.

Conceptually:

```text
Gazebo physics
      ↓
actual simulated robot pose
      ↓
ground truth
```

The experiment will compare:

```text
Custom Odometry             Gazebo Ground Truth

x_odom                      x_true
y_odom          vs          y_true
theta_odom                  theta_true
```

---

## 2. Why /odom and TF Agreement Is Not Enough

Previously I verified:

```text
/odom
```

and:

```text
odom -> base_link TF
```

in RViz.

They agreed.

However, this does not prove that the odometry is accurate because both outputs are generated using the same:

```python
self.x
self.y
self.theta
```

Therefore:

```text
/odom agrees with TF
        ↓
internal consistency verified
```

but:

```text
/odom agrees with TF
        ≠
physical accuracy verified
```

For accuracy, I need an independent reference.

That independent reference is Gazebo ground truth.

---

## 3. Finding the Gazebo Ground-Truth Topic

I searched Gazebo pose topics using:

```bash
gz topic -l | grep -E 'pose|dynamic_pose'
```

The output included:

```text
/gui/camera/pose
/world/restaurant_world/dynamic_pose/info
/world/restaurant_world/pose/info
```

`/gui/camera/pose` is only the Gazebo GUI camera position, so it is not useful for robot ground truth.

The useful topic is:

```text
/world/restaurant_world/dynamic_pose/info
```

---

## 4. Gazebo Dynamic Pose

I echoed:

```bash
gz topic -e -t /world/restaurant_world/dynamic_pose/info
```

and found:

```text
pose {
  name: "restaurant_robot"
  id: 14
  position {
    x: 2.8505772648917045
    y: 1.3059666326000507
    z: 0.050000056792530445
  }
  orientation {
    x: ...
    y: ...
    z: 0.9934076939201707
    w: 0.11463487104803094
  }
}
```

At that moment Gazebo's physics system believed the robot was approximately at:

```text
x = 2.851 m
y = 1.306 m
z = 0.050 m
```

This gives me an independent robot pose for the experiment.

---

## 5. Why Gazebo Also Shows base_link and Wheels

The topic also contained:

```text
restaurant_robot
base_link
left_wheel
right_wheel
```

The robot is made from multiple entities.

Conceptually:

```text
restaurant_robot
│
├── base_link
├── left_wheel
└── right_wheel
```

The `restaurant_robot` model pose tells me where the full robot model is located in the Gazebo world.

The `base_link` entry appeared approximately as:

```text
position = 0, 0, 0
orientation.w = 1
```

because it is located at the robot model origin relative to its parent.

This does not mean the whole robot is at world position zero.

---

## 6. Wheel Geometry Observation

Gazebo showed approximately:

```text
left wheel y  = +0.30 m
right wheel y = -0.30 m
```

Therefore:

```text
distance between wheels = 0.60 m
```

This agrees with the wheel separation used in my robot model:

```text
wheel_separation = 0.60 m
```

---

## 7. Gazebo Pose Message Type

Inspecting the topic showed:

```text
gz.msgs.Pose_V
```

This explains why one Gazebo message contains multiple poses.

It can contain poses for:

```text
restaurant_robot
base_link
left_wheel
right_wheel
...
```

---

# Coordinate Alignment Before Comparison

A very important concept today was understanding why I cannot directly compare raw Gazebo coordinates with custom odometry coordinates.

My custom odometry begins from:

```text
x = 0
y = 0
theta = 0
```

But Gazebo may say that the robot starts at:

```text
x = 2.85
y = 1.31
```

This does not mean the odometry already has a 2.85 m error.

The systems simply have different coordinate origins.

---

## 8. Different Origins Can Describe the Same Robot

Example:

```text
Odometry start:
x = 0 m

Gazebo start:
x = 5 m
```

Then the robot moves.

Gazebo later says:

```text
x = 7 m
```

The robot actually moved:

```text
7 - 5 = 2 m
```

So I should compare the **change in position**, not the raw absolute coordinates.

For Gazebo:

```text
Gazebo displacement
=
Gazebo final position
-
Gazebo starting position
```

Example:

```text
7 m - 5 m = 2 m
```

Custom odometry might report:

```text
1.96 m
```

Then the meaningful comparison becomes:

```text
Gazebo true displacement = 2.00 m
Odometry estimate        = 1.96 m
```

---

## 9. Same Numerical Origin Is Not Required

The important lesson is:

> The two systems do not need to start with the same numerical coordinates.

They must describe the same physical motion using compatible coordinate frames.

It is possible for:

```text
Odometry: x = 0
Gazebo:   x = 5
```

to both be correct at the same physical starting location.

They simply use different origins.

---

## 10. Axis Orientation Also Matters

Origin is not the only issue.

Coordinate-axis direction also matters.

For example:

```text
Gazebo +x →

Odometry +x
     ↑
```

A robot moving forward by 1 m could then appear as:

```text
Odometry:
x = 1
y = 0
```

while Gazebo could describe the same physical motion as:

```text
x = 0
y = 1
```

Neither one is necessarily wrong.

The coordinate systems may simply be rotated relative to each other.

Therefore alignment involves:

```text
1. Origin alignment

2. Orientation / axis alignment
```

For the first baseline experiment, I will try to keep the robot starting orientation simple so that the comparison is easier.

---

# Odometry Error

For a simple straight-line experiment:

```text
true distance = Gazebo displacement
estimated distance = odometry displacement
```

I defined signed odometry error as:

```text
error = odometry distance - true distance
```

---

## 11. Positive Error

Example:

```text
Gazebo = 1.50 m
Odom   = 1.57 m
```

Then:

```text
error = 1.57 - 1.50
      = +0.07 m
```

The odometry **overestimated** the travelled distance by:

```text
0.07 m = 7 cm
```

So:

```text
positive error
→ odometry estimate is larger than ground truth
```

---

## 12. Negative Error

Example:

```text
Gazebo = 2.00 m
Odom   = 1.92 m
```

Then:

```text
error = 1.92 - 2.00
      = -0.08 m
```

The odometry **underestimated** the travelled distance by:

```text
0.08 m = 8 cm
```

So:

```text
negative error
→ odometry estimate is smaller than ground truth
```

---

# Error Does Not Automatically Mean Wheel Slip

An important correction today:

```text
odometry error
≠
automatically wheel slip
```

Possible causes include:

- wheel slip
- incorrect wheel radius
- incorrect wheel separation
- collision
- measurement noise
- simulation/model mismatch
- numerical approximation
- timing differences

The experiment tells me that an error exists.

Further experiments help identify the cause.

---

# Error Over Time

Only comparing the final position can hide useful information.

For example:

```text
True Distance    Odom Distance    Error

0.0 m            0.00 m           0.00 m
1.0 m            1.01 m           0.01 m
2.0 m            2.03 m           0.03 m
3.0 m            3.05 m           0.05 m
4.0 m            4.08 m           0.08 m
5.0 m            5.11 m           0.11 m
```

This shows the error gradually increasing.

A final measurement alone would only tell me:

```text
final error = 0.11 m
```

But measurements over time show:

```text
how the error developed
```

---

# Gradual Drift vs Sudden Error Jump

## Gradual Drift

Gradual drift means the estimation error slowly accumulates.

Possible causes:

- slightly incorrect wheel radius
- slightly incorrect wheel separation
- repeated small wheel slip
- repeated measurement errors

Example pattern:

```text
small error
   ↓
small error
   ↓
slightly larger error
   ↓
larger accumulated error
```

---

## Sudden Error Jump

A sudden error jump may occur after an abrupt physical event.

Examples:

- collision
- large wheel slip
- wheels spinning while the robot is stuck
- robot being pushed

Example:

```text
error almost zero
      ↓
robot hits obstacle
      ↓
wheels continue rotating
      ↓
body does not move as expected
      ↓
odometry continues adding movement
      ↓
error suddenly increases
```

This kind of error graph can help identify **when** something went wrong.

---

# Systematic vs Random Error

## Systematic / Repeatable Bias

Suppose I repeat a 2 m experiment five times and get:

```text
-0.06 m
-0.05 m
-0.06 m
-0.07 m
-0.06 m
```

The similar errors suggest a repeatable systematic bias.

Possible causes:

```text
wheel radius calibration
wheel separation calibration
conversion assumption
consistent model mismatch
```

---

## Random Error

If repeated trials produce:

```text
-0.01 m
+0.04 m
-0.03 m
+0.02 m
-0.05 m
```

the error changes unpredictably.

This suggests random variation.

Possible causes could include:

- unpredictable slip
- contact variation
- measurement noise
- timing differences

The important distinction is:

```text
similar error each run
→ systematic / repeatable bias

unpredictable changing error
→ random variation
```

---

# Why Repeat Experiments?

One trial can be misleading.

Repeating the same test helps separate:

```text
systematic bias
```

from:

```text
random variation
```

This is an important step toward experimental robotics rather than only implementation.

---

# Wheel Radius and Distance Error

Wheel distance is calculated using:

```text
Δs = r × Δφ
```

Where:

```text
r = wheel radius
Δφ = wheel-angle change
```

---

## Wheel Radius Too Large

If the radius used by the odometry code is too large:

```text
calculated Δs becomes too large
```

Therefore:

```text
odometry distance > true distance
```

The robot appears to have travelled farther than it really did.

This tends to produce positive distance error.

---

## Wheel Radius Too Small

If the radius used in the odometry code is too small:

```text
calculated Δs becomes too small
```

Therefore:

```text
odometry distance < true distance
```

The odometry underestimates how far the robot travelled.

---

# Planned Baseline Experiment

The first practical experiment will be a simple straight-line test.

```text
Start robot
      ↓
record odometry starting pose
      ↓
record Gazebo starting pose
      ↓
move robot straight
      ↓
stop robot
      ↓
record odometry final pose
      ↓
record Gazebo final pose
      ↓
calculate displacement
      ↓
compare estimate with ground truth
      ↓
calculate odometry error
```

The first test will use the current correct robot parameters.

I will not intentionally introduce wheel-radius errors until I establish the clean baseline.

---

# Simulation Setup

Gazebo world:

```bash
gz sim ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_description/worlds/restaurant_world.sdf
```

Spawn robot:

```bash
gz service -s /world/restaurant_world/create \
--reqtype gz.msgs.EntityFactory \
--reptype gz.msgs.Boolean \
--timeout 15000 \
--req 'sdf_filename: "/home/pradip/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_description/models/restaurant_robot.sdf", name: "restaurant_robot", pose: {position: {x: 0, y: 0, z: 0.5}}'
```

JointState bridge:

```bash
source /opt/ros/jazzy/setup.bash

ros2 run ros_gz_bridge parameter_bridge \
'/world/restaurant_world/model/restaurant_robot/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'
```

Custom odometry:

```bash
source /opt/ros/jazzy/setup.bash

cd ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status

python3 odometry_node.py
```

Straight movement:

```bash
gz topic -t /cmd_vel \
-m gz.msgs.Twist \
-p 'linear: {x: 0.2}, angular: {z: 0.0}'
```

Stop:

```bash
gz topic -t /cmd_vel \
-m gz.msgs.Twist \
-p 'linear: {x: 0.0}, angular: {z: 0.0}'
```

---

# Current Debugging Issue

When I tried:

```bash
ros2 topic echo /odom --once
```

no message was printed.

The JointState echo also stopped printing.

Because of limited study time, I stopped here instead of rushing through the debugging.

This does **not** change the conceptual progress of today's session.

The next session should begin by checking the data chain:

```text
Gazebo JointStatePublisher
        ↓
Gazebo joint_state topic
        ↓
ros_gz_bridge
        ↓
ROS2 JointState topic
        ↓
odometry_node.py
        ↓
/odom
```

Useful checks:

```bash
ros2 topic list | grep -E 'odom|joint'
```

```bash
ros2 topic echo /world/restaurant_world/model/restaurant_robot/joint_state --once
```

```bash
ros2 node list | grep odom
```

The goal is to identify where the message chain has stopped before continuing the experiment.

---

# What I Learned Today

Today I moved from thinking only about whether odometry "works" toward thinking about how to evaluate its accuracy.

The important ideas were:

1. `/odom` and TF agreeing only proves internal consistency.

2. Gazebo ground truth gives an independent reference.

3. Raw coordinates cannot always be compared directly because coordinate origins may differ.

4. Relative displacement can be compared even when starting coordinate values are different.

5. Coordinate-axis orientation also matters.

6. Positive signed error means odometry overestimated distance.

7. Negative signed error means odometry underestimated distance.

8. Error is not automatically caused by wheel slip.

9. Gradual drift and sudden error jumps can indicate different physical problems.

10. Repeated experiments help separate systematic bias from random variation.

11. Incorrect wheel radius can create systematic distance error.

12. Measuring error throughout a trajectory provides much more information than only checking the final point.

---

# Learning Evidence

Today I:

- identified Gazebo's dynamic pose topic
- extracted the `restaurant_robot` ground-truth pose
- understood the `gz.msgs.Pose_V` message
- distinguished model pose from link-relative pose
- connected wheel positions to the configured 0.60 m wheel separation
- learned why coordinate origins must be aligned before comparison
- learned why orientation alignment also matters
- defined signed odometry distance error
- distinguished overestimation from underestimation
- distinguished gradual drift from sudden error jumps
- distinguished systematic bias from random variation
- understood why repeated trials are necessary
- connected wheel-radius calibration to systematic odometry error
- designed the structure of the first straight-line baseline experiment

---

# Resume Point

Next session:

```text
1. Restore JointState communication
2. Confirm /odom is publishing
3. Record initial custom odometry pose
4. Record initial Gazebo ground-truth pose
5. Run one controlled straight-line movement
6. Record final poses
7. Calculate true displacement
8. Calculate estimated displacement
9. Calculate odometry error
10. Repeat the experiment
```

The immediate technical issue to solve first is:

```text
JointState / /odom messages are currently not printing
```

After that, continue the straight-line baseline experiment.
