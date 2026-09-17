# Day 58 – Custom Differential-Drive Odometry Complete

Date: 17 September 2026

## Goal

Complete and verify the full custom differential-drive odometry chain for my ROS2 restaurant delivery robot.

Today I completed:

- Linear velocity calculation
- Angular velocity calculation
- `/odom` pose publishing
- `/odom` twist publishing
- `odom -> base_link` TF broadcasting
- RViz visualization
- Verification that `/odom` and TF agree

---

## Complete Odometry Pipeline

```text
Gazebo wheel joints
        ↓
sensor_msgs/JointState
        ↓
left/right wheel angles
        ↓
delta wheel angles
        ↓
wheel distances
        ↓
delta_s + delta_theta
        ↓
delta_x + delta_y
        ↓
x + y + theta
        ↓
delta_t
        ↓
linear velocity + angular velocity
        ↓
nav_msgs/Odometry
        ↓
/odom
        ↓
TransformStamped
        ↓
odom -> base_link
        ↓
RViz
```

---

## Time Difference

Velocity needs time.

I added:

```python
self.previous_time = None
```

Current time comes from the JointState timestamp:

```python
current_time = (
    msg.header.stamp.sec +
    msg.header.stamp.nanosec * 1e-9
)
```

Then:

```python
delta_t = current_time - self.previous_time
```

I also protect against invalid time:

```python
if delta_t <= 0.0:
    return
```

At the end of each callback:

```python
self.previous_time = current_time
```

This means every callback compares its timestamp with the previous measurement.

---

## Linear Velocity

The robot center movement is:

```text
delta_s
```

Linear velocity:

```python
linear_velocity = delta_s / delta_t
```

Equation:

```text
v = delta_s / delta_t
```

Unit:

```text
m/s
```

Physical meaning:

Linear velocity tells how fast the robot is moving forward or backward.

```text
positive v = forward
negative v = backward
```

---

## Angular Velocity

The robot orientation change is:

```text
delta_theta
```

Angular velocity:

```python
angular_velocity = delta_theta / delta_t
```

Equation:

```text
omega = delta_theta / delta_t
```

Unit:

```text
rad/s
```

Physical meaning:

Angular velocity tells how fast the robot orientation is changing.

```text
positive omega = counter-clockwise / left
negative omega = clockwise / right
```

---

## Pose Calculation

The robot pose is updated using:

```python
theta_mid = self.theta + delta_theta / 2.0

delta_x = delta_s * math.cos(theta_mid)
delta_y = delta_s * math.sin(theta_mid)

self.x += delta_x
self.y += delta_y
self.theta += delta_theta
```

The node maintains:

```text
x
y
theta
```

inside the `odom` frame.

---

## ROS2 /odom Message

The node creates:

```python
odom_msg = Odometry()
```

I use the JointState measurement timestamp:

```python
odom_msg.header.stamp = msg.header.stamp
```

Frames:

```python
odom_msg.header.frame_id = 'odom'
odom_msg.child_frame_id = 'base_link'
```

Meaning:

```text
The pose of base_link is described relative to odom.
```

---

## Position in /odom

```python
odom_msg.pose.pose.position.x = self.x
odom_msg.pose.pose.position.y = self.y
odom_msg.pose.pose.position.z = 0.0
```

The current robot uses planar 2D odometry.

---

## Theta to Quaternion

ROS2 orientation uses a quaternion rather than storing theta directly.

For planar motion:

```python
odom_msg.pose.pose.orientation.x = 0.0
odom_msg.pose.pose.orientation.y = 0.0
odom_msg.pose.pose.orientation.z = math.sin(self.theta / 2.0)
odom_msg.pose.pose.orientation.w = math.cos(self.theta / 2.0)
```

So:

```text
theta
  ↓
quaternion
  ↓
ROS2 orientation
```

---

## Twist in /odom

I added:

```python
odom_msg.twist.twist.linear.x = linear_velocity
odom_msg.twist.twist.angular.z = angular_velocity
```

Therefore `/odom` now contains both:

```text
pose
→ where the robot estimates it is

twist
→ how the robot estimates it is moving
```

Then:

```python
self.odom_publisher.publish(odom_msg)
```

publishes the message.

---

## Velocity Verification

I commanded approximately:

```text
linear velocity = 0.2 m/s
angular velocity = 0.3 rad/s
```

My custom odometry produced approximately:

```text
linear.x = 0.2000 m/s
angular.z = 0.3000 rad/s
```

This verified:

```text
v = delta_s / delta_t
```

and:

```text
omega = delta_theta / delta_t
```

When the robot was stopped, extremely small values such as:

```text
3e-14
2e-19
```

appeared.

These are effectively zero and come from floating-point numerical precision.

---

## TF Broadcaster

I imported:

```python
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
```

Inside `__init__()`:

```python
self.tf_broadcaster = TransformBroadcaster(self)
```

Inside the callback:

```python
transform_msg = TransformStamped()
```

Then:

```python
transform_msg.header.stamp = msg.header.stamp
transform_msg.header.frame_id = 'odom'
transform_msg.child_frame_id = 'base_link'
```

Translation:

```python
transform_msg.transform.translation.x = self.x
transform_msg.transform.translation.y = self.y
transform_msg.transform.translation.z = 0.0
```

Rotation:

```python
transform_msg.transform.rotation.x = 0.0
transform_msg.transform.rotation.y = 0.0
transform_msg.transform.rotation.z = math.sin(self.theta / 2.0)
transform_msg.transform.rotation.w = math.cos(self.theta / 2.0)
```

Finally:

```python
self.tf_broadcaster.sendTransform(transform_msg)
```

This creates:

```text
odom
  ↓
base_link
```

---

## TF Verification

I tested:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

ROS2 successfully returned changing translation and rotation values.

Example:

```text
Translation: [0.191, 0.028, 0.000]

Rotation RPY:
yaw = 0.291 rad
```

Later:

```text
Translation: [0.619, 0.418, 0.000]

yaw = 1.189 rad
```

This confirmed that the `odom -> base_link` transform was working.

---

## RViz Verification

I started RViz:

```bash
rviz2
```

Set:

```text
Global Options
→ Fixed Frame = odom
```

Added:

```text
TF
Odometry
```

For Odometry:

```text
Topic = /odom
```

For clear verification I used:

```text
Odometry Keep = 1

TF Show Names = ON
TF Show Axes = ON
```

RViz successfully displayed:

```text
odom
base_link
```

and the latest `/odom` pose arrow.

---

## /odom and TF Agreement

Both `/odom` and TF use the same:

```text
self.x
self.y
self.theta
```

Therefore:

```text
/odom pose
and
odom -> base_link TF
```

should describe the same estimated robot pose.

I visually verified in RViz that:

```text
latest /odom arrow position
≈
base_link TF position
```

and:

```text
/odom arrow direction
≈
base_link forward x-axis direction
```

while the robot moved.

---

## Motion Cases Verified

### Straight Motion

```text
position changes
theta stays almost constant
```

### Backward Motion

```text
linear velocity becomes negative
```

### In-Place Rotation

```text
x/y stay nearly constant
theta changes
```

### Curved Motion

```text
x changes
y changes
theta changes
```

### Left Rotation

```text
angular velocity is positive
```

### Right Rotation

```text
angular velocity is negative
```

---

## Final Architecture

```text
Gazebo robot
      ↓
wheel joints
      ↓
JointStatePublisher
      ↓
ros_gz_bridge
      ↓
sensor_msgs/JointState
      ↓
odometry_node.py
      ↓
delta_phi_L / delta_phi_R
      ↓
delta_s_L / delta_s_R
      ↓
delta_s / delta_theta
      ↓
delta_x / delta_y
      ↓
x / y / theta
      ↓
delta_t
      ↓
v / omega
      ↓
      ├───────────────┐
      ↓               ↓
nav_msgs/Odometry     TF
      ↓               ↓
    /odom       odom -> base_link
      └───────┬───────┘
              ↓
             RViz
```

---

## What I Learned

Odometry is not simply reading the robot position.

The robot estimates its movement from wheel rotation.

Each callback represents a very small amount of wheel movement.

These small movements are accumulated over time to estimate:

```text
x
y
theta
```

Velocity requires the time between measurements:

```text
v = delta_s / delta_t

omega = delta_theta / delta_t
```

`/odom` contains numerical odometry information.

TF describes the relationship between coordinate frames.

Both `/odom` and TF can describe the same robot pose, but they serve different purposes in ROS2.

---

## Important Limitation

Completing wheel odometry does not mean the robot knows its true global position.

Wheel odometry can drift because of:

- wheel slip
- collisions
- inaccurate wheel radius
- inaccurate wheel separation
- uneven floors
- encoder errors
- wheel wear

Therefore:

```text
odometry estimate != guaranteed ground truth
```

External sensing and localization will later be needed to correct accumulated errors.

---

## Milestone Completed

Custom differential-drive wheel odometry:

```text
IMPLEMENTED
TESTED
PUBLISHED
TF BROADCAST
RVIZ VERIFIED
```

The robot can now estimate:

```text
position
orientation
linear velocity
angular velocity
```

from wheel joint measurements.

---

## Learning Evidence

I built a custom ROS2 differential-drive odometry node instead of relying only on ready-made odometry output.

The node now:

- receives simulated wheel joint measurements
- calculates wheel angle changes
- converts wheel rotation into wheel displacement
- calculates robot center translation
- calculates robot orientation change
- estimates x, y and theta
- calculates linear velocity
- calculates angular velocity
- publishes `nav_msgs/Odometry` on `/odom`
- broadcasts `odom -> base_link`
- visualizes the estimate in RViz
- verifies that `/odom` and TF represent the same estimated pose

This completes the core wheel-odometry implementation for my restaurant delivery robot.

---

## Next Research Step

The next useful experiment is to compare:

```text
custom wheel odometry
vs
Gazebo ground truth
```

and measure error under different conditions.

Possible experiments:

- clean straight movement
- curved movement
- wheel slip
- collision with an obstacle
- incorrect wheel-radius parameter
- incorrect wheel-separation parameter

This will turn the odometry implementation into experimental evidence about drift, uncertainty and the need for localization.
