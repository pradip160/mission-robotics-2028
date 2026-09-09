# Day 50 – Odometry: Angular Velocity, Linear Velocity and Orientation

**Date:** September 9, 2026
**Mission:** Korea 2028
**Main Topic:** Differential-drive odometry foundations

## 1. Wheel Angle Change

The wheel's angular position is represented by:

$$
\phi
$$

The change in wheel angle is:

$$
\Delta\phi = \phi_{new} - \phi_{old}
$$

Example:

If the encoder changes from:

$$
5\text{ rad} \rightarrow 9\text{ rad}
$$

then:

$$
\Delta\phi = 9-5 = 4\text{ rad}
$$

This means the wheel physically rotated through **4 radians** during that interval.

---

## 2. Angular Velocity

Angular velocity tells how fast an angle is changing with time.

$$
\omega = \frac{\Delta\phi}{\Delta t}
$$

Unit:

$$
rad/s
$$

Example:

If:

$$
\Delta\phi=6\text{ rad}
$$

during:

$$
\Delta t=2s
$$

then:

$$
\omega=\frac{6}{2}=3\text{ rad/s}
$$

Physical meaning:

The wheel is rotating at an average rate of **3 radians every second**.

Important distinction:

* \(\phi\) = current/accumulated wheel angle
* \(\Delta\phi\) = change in wheel angle
* \(\omega\) = angular velocity
* \(\Delta\omega\) = change in angular velocity

For example, if:

$$
\omega_{old}=3\text{ rad/s}
$$

and:

$$
\omega_{new}=4\text{ rad/s}
$$

then:

$$
\Delta\omega=1\text{ rad/s}
$$

---

## 3. Wheel Angular Velocity to Linear Velocity

A spinning wheel creates linear motion along the ground.

The relationship is:

$$
v=r\omega
$$

where:

* \(v\) = linear wheel velocity \([m/s]\)
* \(r\) = wheel radius \([m]\)
* \(\omega\) = wheel angular velocity \([rad/s]\)

Example:

$$
r=0.2m
$$

$$
\omega=3\text{ rad/s}
$$

therefore:

$$
v=0.2\times3=0.6\text{ m/s}
$$

Physical meaning:

Assuming no wheel slip, the wheel is moving along the ground at **0.6 metres per second**.

---

## 4. Left and Right Wheel Velocities

For a differential-drive robot:

$$
v_L=r\omega_L
$$

$$
v_R=r\omega_R
$$

Example:

$$
r=0.1m
$$

$$
\omega_L=4\text{ rad/s}
$$

$$
\omega_R=6\text{ rad/s}
$$

Then:

$$
v_L=0.4\text{ m/s}
$$

$$
v_R=0.6\text{ m/s}
$$

Because the right wheel moves faster than the left wheel, the robot curves toward the **left**.

The robot tends to curve toward the slower wheel.

---

## 5. Robot Centre Linear Velocity

The forward velocity of the robot centre is the average of the two wheel velocities:

$$
v_{robot}=\frac{v_R+v_L}{2}
$$

For:

$$
v_L=0.4\text{ m/s}
$$

$$
v_R=0.6\text{ m/s}
$$

we get:

$$
v_{robot}
=
\frac{0.6+0.4}{2}
=
0.5\text{ m/s}
$$

Physical meaning:

The robot centre is moving forward at approximately **0.5 m/s**.

---

## 6. Whole-Robot Angular Velocity

The robot's turning velocity is:

$$
\omega_{robot}
=
\frac{v_R-v_L}{b}
$$

where \(b\) is the wheelbase.

Example:

$$
v_R=0.6\text{ m/s}
$$

$$
v_L=0.4\text{ m/s}
$$

$$
b=0.5m
$$

Then:

$$
\omega_{robot}
=
\frac{0.6-0.4}{0.5}
=
0.4\text{ rad/s}
$$

Physical meaning:

The whole robot's heading is changing at **0.4 radians per second**.

Important:

$$
\omega_L,\omega_R
$$

describe how fast the **wheels spin**.

$$
\omega_{robot}
$$

describes how fast the **whole robot changes orientation**.

---

## 7. Velocity vs Distance

Linear velocity:

$$
v
$$

has unit:

$$
m/s
$$

Distance change is:

$$
\Delta s=v\Delta t
$$

and has unit:

$$
m
$$

Example:

$$
v=0.5\text{ m/s}
$$

for:

$$
\Delta t=2s
$$

gives:

$$
\Delta s=0.5\times2=1m
$$

So the robot travelled **1 metre**, not 1 m/s.

---

## 8. Angular Velocity vs Orientation Change

Angular velocity:

$$
\omega
$$

has unit:

$$
rad/s
$$

Orientation change is:

$$
\Delta\theta=\omega\Delta t
$$

and has unit:

$$
rad
$$

Example:

$$
\omega=0.4\text{ rad/s}
$$

for:

$$
\Delta t=2s
$$

gives:

$$
\Delta\theta=0.8\text{ rad}
$$

So the robot's heading changed by **0.8 radians**.

---

## 9. Meaning of Positive and Negative Signs

For linear velocity:

$$
v>0
$$

means the robot moves **forward** relative to its own front.

$$
v<0
$$

means the robot moves **backward** relative to its own front.

For angular velocity:

$$
\omega>0
$$

means counter-clockwise / left rotation.

$$
\omega<0
$$

means clockwise / right rotation.

Example:

$$
v=-0.4\text{ m/s}
$$

means the robot drives backward.

$$
\omega=+0.3\text{ rad/s}
$$

means the robot rotates counter-clockwise/left at the same time.

---

## 10. Signed Distance and Orientation Changes

Given:

$$
v=-0.5\text{ m/s}
$$

$$
\omega=-0.4\text{ rad/s}
$$

for:

$$
\Delta t=2s
$$

then:

$$
\Delta s=-1m
$$

and:

$$
\Delta\theta=-0.8\text{ rad}
$$

Physical interpretation:

The robot moved **1 metre backward** while its heading rotated **0.8 radians clockwise/right**.

---

## 11. Updating Robot Orientation

Orientation is updated using:

$$
\theta_{new}
=
\theta_{old}+\Delta\theta
$$

Example:

$$
\theta_{old}=0.5\text{ rad}
$$

$$
\Delta\theta=-0.8\text{ rad}
$$

therefore:

$$
\theta_{new}=-0.3\text{ rad}
$$

Important correction:

A negative \(\theta\) does **not** mean the robot is facing backward.

It means the robot's orientation is clockwise from the chosen reference direction.

$$
-0.3\text{ rad}\approx-17^\circ
$$

So it is only facing about 17° clockwise from the reference direction.

---

## 12. Robot Front vs Orientation vs Motion

These are three different concepts.

### Robot Front

The physical robot has a defined front.

In ROS, the `base_link` frame normally uses its positive x-axis as the robot's forward direction.

### Orientation \(\theta\)

\(\theta\) answers:

> Which direction is the robot's front currently pointing relative to the reference frame?

### Linear Velocity \(v\)

\(v\) answers:

> Is the robot travelling forward or backward relative to its own front?

Therefore, a robot can face one direction while driving backward without changing its orientation.

---

## 13. Initial Coordinate Reference

The robot does not require a universal world coordinate system to begin odometry.

At startup we can define:

$$
x=0,\qquad y=0,\qquad\theta=0
$$

This means:

* wherever the robot starts becomes the initial position
* its starting front direction becomes the reference orientation

The robot then estimates all future motion relative to this initial reference.

---

## 14. Travelling Into New Environments

The coordinate frame does not need to restart when the robot enters another room.

The robot repeatedly performs:

```text
previous pose
    ↓
new wheel encoder measurements
    ↓
calculate motion change
    ↓
Δx, Δy, Δθ
    ↓
update pose
    ↓
new pose
```

So the robot can travel from a kitchen into a corridor and then into a dining room while continuing to estimate its pose relative to the original reference.

---

## 15. Odometry Is Still an Estimate

If the robot travels for a long distance, odometry error can accumulate because of:

* wheel slip
* incorrect wheel radius
* wheelbase error
* encoder error/resolution
* uneven surfaces
* wheel wear
* external forces

Therefore, odometry might estimate one position while the real robot is slightly somewhere else.

External sensing such as:

* LiDAR
* camera
* IMU
* localization
* SLAM

can later help correct this error.

---

## 16. Connection to SLAM

A robot does not need an existing map to start.

It can begin from:

$$
(x,y,\theta)=(0,0,0)
$$

and use odometry to estimate motion.

At the same time, sensors such as LiDAR can observe walls and obstacles.

SLAM allows the robot to:

1. build a map of an unknown environment
2. estimate its own location inside that map

This connects today's odometry concepts directly to the future SLAM work.

---

## Key Learning Chain

Today I connected:

```text
Encoder wheel angle
        ↓
Δφ
        ↓
ω = Δφ / Δt
        ↓
v = rω
        ↓
vL and vR
        ↓
robot linear velocity
+
robot angular velocity
        ↓
Δs and Δθ
        ↓
pose/orientation update
```

This helped me understand that odometry is not just formulas. It is a chain that converts **physical wheel measurements into an estimate of robot motion and pose**.

## Important Corrections From Today

I initially confused:

* wheel angle with angular velocity
* angular velocity with change in angular velocity
* metres with metres per second
* radians with radians per second
* negative orientation with facing backward

The important distinctions are now:

$$
\Delta\phi\ [rad]
$$

= wheel angle change

$$
\omega\ [rad/s]
$$

= angular velocity

$$
v\ [m/s]
$$

= linear velocity

$$
\Delta s\ [m]
$$

= distance change

$$
\Delta\theta\ [rad]
$$

= orientation change

Negative linear velocity means backward motion.

Negative angular velocity/orientation change means clockwise rotation, not automatically backward motion.

## Learning Evidence

I solved multiple examples involving:

* wheel-angle changes
* angular velocity
* wheel linear velocity
* differential-drive left/right wheel speeds
* robot centre velocity
* whole-robot angular velocity
* signed forward/backward motion
* signed left/right rotation
* distance and orientation changes
* pose orientation updates

I also questioned how a robot knows its orientation when there is no world map, which led to understanding the idea of an **initial coordinate reference frame** and its connection to odometry and SLAM.

**Video evidence:** Add today's YouTube/demo link here.

## Next Session

Continue from the coordinate-frame question.

Main checkpoint:

A robot starts at:

$$
(x,y,\theta)=(0,0,0)
$$

It rotates left until:

$$
\theta=\frac{\pi}{2}
$$

and then completely stops:

$$
v=0
$$

Next session I should explain:

1. which direction the robot is facing
2. whether stopping causes the robot to lose its orientation
3. difference between `odom`, `base_link`, and later `map`
4. how pose remains meaningful while the robot is stationary

Then continue toward full differential-drive odometry and ROS2 implementation.

