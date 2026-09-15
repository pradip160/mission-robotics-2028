# Day 56 – Odometry Pose and ROS2 /odom

Date: 15 September 2026

## Goal

Continue custom differential-drive odometry.

Today I moved from wheel movement calculations to:

- x, y, theta pose estimation
- straight-motion testing
- rotation testing
- curved-motion testing
- publishing the pose to ROS2 `/odom`

---

## 1. Complete Odometry Pipeline

```text
Wheel angles
phi_L, phi_R
      ↓
Wheel angle changes
delta_phi_L, delta_phi_R
      ↓
Wheel distances
delta_s_L, delta_s_R
      ↓
Robot center movement
delta_s
      ↓
Orientation change
delta_theta
      ↓
Midpoint heading
theta_mid
      ↓
delta_x, delta_y
      ↓
x, y, theta
      ↓
Quaternion
      ↓
nav_msgs/Odometry
      ↓
/odom
2. Robot Parameters

My robot uses:

self.wheel_radius = 0.10
self.wheel_separation = 0.60

So:

wheel radius = 0.10 m
wheel separation = 0.60 m
3. Wheel Angle Change

The node receives wheel angles from JointState.

delta_left_angle = left_angle - self.previous_left_angle
delta_right_angle = right_angle - self.previous_right_angle

Equation:

delta_phi = current_angle - previous_angle

Odometry needs the change in wheel rotation, not only the total wheel angle.

4. Wheel Rotation to Distance
delta_left_distance = self.wheel_radius * delta_left_angle
delta_right_distance = self.wheel_radius * delta_right_angle

Equation:

delta_s = radius * delta_phi

Example:

radius = 0.10 m
delta_phi = -0.002 rad

delta_s = -0.0002 m

Negative distance means backward wheel movement.

5. Robot Center Movement
delta_s = (
    delta_right_distance + delta_left_distance
) / 2.0

Equation:

delta_s = (delta_s_R + delta_s_L) / 2

This gives the movement of the center of the robot.

If both wheels move the same distance, the robot moves straight.

6. Orientation Change
delta_theta = (
    delta_right_distance - delta_left_distance
) / self.wheel_separation

Equation:

delta_theta =
(delta_s_R - delta_s_L) / wheel_separation

If both wheels move equally:

delta_theta = 0

If the right wheel moves farther:

delta_theta > 0
robot turns left

If the left wheel moves farther:

delta_theta < 0
robot turns right
7. Pose State

Inside __init__():

self.x = 0.0
self.y = 0.0
self.theta = 0.0

The robot's starting position is treated as the odometry origin:

x = 0
y = 0
theta = 0
8. Midpoint Heading

For curved movement:

theta_mid = self.theta + delta_theta / 2.0

The robot changes heading during the small movement.

Using the heading halfway through the movement gives a better estimate of its direction.

9. Convert Robot Movement to x and y

Required import:

import math

Pose projection:

delta_x = delta_s * math.cos(theta_mid)
delta_y = delta_s * math.sin(theta_mid)

Equations:

delta_x = delta_s * cos(theta_mid)

delta_y = delta_s * sin(theta_mid)

The robot moves forward in its own base_link frame.

But odometry position is measured in the fixed odom frame.

cos() and sin() convert robot-forward movement into odom x/y movement.

10. Accumulate Pose
self.x += delta_x
self.y += delta_y
self.theta += delta_theta

Meaning:

new_x = old_x + delta_x

new_y = old_y + delta_y

new_theta = old_theta + delta_theta

Odometry builds the robot pose by accumulating many tiny movements.

11. Straight Motion Test

I drove the robot straight forward.

Example output:

Pose -> x: 2.9692 m | y: 0.0000 m | theta: 0.0000 rad
Pose -> x: 2.9694 m | y: 0.0000 m | theta: 0.0000 rad
Pose -> x: 2.9696 m | y: 0.0000 m | theta: 0.0000 rad

Result:

x increased
y stayed near zero
theta stayed zero

Reason:

left wheel distance = right wheel distance

Therefore:

delta_theta = 0

The robot moved straight.

12. In-Place Left Rotation Test

Command:

gz topic -t /cmd_vel \
-m gz.msgs.Twist \
-p 'linear: {x: 0.0}, angular: {z: 0.5}'

Observed:

x ≈ 0
y ≈ 0

theta:
1.5300
1.5305
1.5310
...
1.5600

So the robot rotated left while its position stayed almost unchanged.

1.57 rad ≈ 90 degrees

This verified the orientation calculation.

13. Curved Motion Test

I also made the robot move forward while turning.

Example output:

x: 0.9683
y: 0.2500
theta: 0.5054

x: 0.9695
y: 0.2507
theta: 0.5061

All three values changed:

x increased
y increased
theta increased

This means:

linear movement + angular movement = curved path

The robot followed an arc.

14. Why x and y Change at Different Rates

The equations are:

delta_x = delta_s * cos(theta)

delta_y = delta_s * sin(theta)

At approximately:

theta = 0.51 rad

the robot was pointing more toward +x than +y.

Therefore:

x increased faster than y

At:

theta = 0.785 rad

which is about:

45 degrees

then:

cos(theta) ≈ sin(theta)

therefore:

delta_x ≈ delta_y
15. ROS2 Odometry Message

Imported:

from nav_msgs.msg import Odometry

Created the publisher:

self.odom_publisher = self.create_publisher(
    Odometry,
    '/odom',
    10
)

Now the odometry node can publish to:

/odom
16. Build the Odometry Message

Inside the callback:

odom_msg = Odometry()

Header:

odom_msg.header.stamp = self.get_clock().now().to_msg()
odom_msg.header.frame_id = 'odom'
odom_msg.child_frame_id = 'base_link'

Meaning:

odom
→ reference frame

base_link
→ robot frame whose pose is being described

So the message describes:

pose of base_link relative to odom
17. Position in the Odometry Message
odom_msg.pose.pose.position.x = self.x
odom_msg.pose.pose.position.y = self.y
odom_msg.pose.pose.position.z = 0.0

This is currently a 2D mobile robot.

Therefore:

z = 0
18. Theta to Quaternion

ROS2 does not store orientation directly as theta.

It stores orientation as a quaternion:

x
y
z
w

For planar robot motion:

odom_msg.pose.pose.orientation.x = 0.0
odom_msg.pose.pose.orientation.y = 0.0
odom_msg.pose.pose.orientation.z = math.sin(self.theta / 2.0)
odom_msg.pose.pose.orientation.w = math.cos(self.theta / 2.0)

Equivalent equations:

qx = 0

qy = 0

qz = sin(theta / 2)

qw = cos(theta / 2)
19. Publish /odom
self.odom_publisher.publish(odom_msg)

I tested:

ros2 topic echo /odom

and ROS2 successfully displayed Odometry messages.

This means my custom odometry node is now publishing /odom.

20. Pose vs Twist

An Odometry message contains both:

pose

and:

twist

Pose answers:

Where is the robot?

It contains:

x
y
orientation

Twist answers:

How is the robot moving right now?

It contains:

linear velocity
angular velocity

Currently I implemented the pose.

My /odom message still shows:

linear velocity = 0.0
angular velocity = 0.0

because I have not implemented the twist fields yet.

21. Covariance

The /odom message also contains covariance values.

Currently they are all:

0.0

I have not implemented uncertainty/covariance yet.

This will be studied later.

22. Bugs Fixed Today
Wrong header capitalization

Wrong:

odom_msg.header.Stamp

Correct:

odom_msg.header.stamp
Wrong position path

Wrong:

odom_msg.pose.position.z

Correct:

odom_msg.pose.pose.position.z
Wrong variable name

Wrong:

odom.msg

Correct:

odom_msg
Wrong spelling

Wrong:

orentation

Correct:

orientation
23. What I Verified
Straight motion
→ position changes
→ theta stays constant

In-place rotation
→ theta changes
→ x/y stay almost constant

Curved motion
→ x, y and theta all change

I also successfully completed:

Gazebo wheel data
      ↓
ROS2 JointState
      ↓
custom odometry calculation
      ↓
x, y, theta
      ↓
quaternion
      ↓
ROS2 /odom
Current System
Gazebo wheel joints
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
quaternion
      ↓
nav_msgs/Odometry
      ↓
/odom
Resume Point

Next study session:

Check one complete message:

ros2 topic echo /odom --once

Verify:

header.frame_id
child_frame_id
position.x
position.y
orientation.z
orientation.w

Then learn:

linear velocity
angular velocity

and fill:

odom_msg.twist.twist.linear.x
odom_msg.twist.twist.angular.z

After /odom is complete:

publish TF
odom -> base_link

Then:

visualize odometry in RViz

Later:

compare custom odometry
against Gazebo ground truth
and measure odometry error
Learning Evidence

Today I completed the first working version of my custom differential-drive odometry pose estimator.

I implemented:

wheel joint angles
→ wheel angle changes
→ wheel distances
→ robot center movement
→ orientation change
→ x/y projection
→ accumulated x, y, theta
→ quaternion
→ ROS2 /odom

I tested the implementation using:

straight movement
in-place rotation
curved movement

The observed pose behavior matched the expected differential-drive motion model.

My custom ROS2 node now calculates the robot pose from wheel movement and publishes it on /odom.
EOF

echo "Saved:"
echo "~/mission-korea/learning-log/2026/Day-56-Odometry-ROS2-Odom/day-56-notes.md"
