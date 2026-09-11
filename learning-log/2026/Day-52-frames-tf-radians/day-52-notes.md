# Day 52 – Coordinate Frames, TF, Radians and Pose Projection

**Date:** September 11, 2026  
**Mission:** Korea 2028  
**Topic:** Odometry foundations – frames, transforms, radians and x/y motion

## 1. base_link

`base_link` is the coordinate frame attached to the robot body.

It moves and rotates with the robot.

For the robot:

- `+x_base` = robot forward direction
- `+y_base` = robot left direction

The important idea is:

> Robot forward does not always mean world/odom +x.

The robot's forward direction depends on its current orientation.

---

## 2. odom Frame

`odom` is a local fixed reference frame used to describe the robot's motion.

The robot moves relative to `odom`.

Example:

If the robot starts at:

\[
(x,y,\theta)=(0,0,0)
\]

and drives forward 3 m without turning:

\[
(x,y,\theta)=(3,0,0)
\]

`odom` stays fixed while `base_link` moves.

A useful mental model:

> `base_link` is like the robot's own view.

> `odom` is like a fixed CCTV view watching the robot move.

---

## 3. map Frame

`map` is used as the corrected global reference.

Odometry can drift because of:

- wheel slip
- wheel radius error
- encoder error
- uneven floor
- accumulated orientation error

Therefore:

\[
odom \rightarrow base\_link
\]

should stay smooth for motion control.

But:

\[
map \rightarrow odom
\]

can be corrected by localization.

The ROS frame relationship is:

\[
map \rightarrow odom \rightarrow base\_link
\]

Meaning:

- `base_link` = robot body frame
- `odom` = smooth local motion estimate
- `map` = corrected long-term/global reference

---

## 4. Why odom → base_link Should Stay Smooth

If the robot is physically moving smoothly, its odometry estimate should also change smoothly.

If software suddenly changes:

\[
odom \rightarrow base\_link
\]

by a large amount, the controller may believe the robot suddenly jumped position even though the real robot did not.

This can cause incorrect motion decisions.

Therefore:

> `odom → base_link` should remain smooth and continuous.

Long-term errors are corrected through:

\[
map \rightarrow odom
\]

instead.

---

## 5. What Is a Transform?

A transform describes the relationship between two coordinate frames.

For a simple 2D robot:

\[
odom \rightarrow base\_link=(x,y,\theta)
\]

Example:

\[
odom \rightarrow base\_link=(4,3,\pi)
\]

means:

- robot is 4 m along odom x
- robot is 3 m along odom y
- robot orientation is \(\pi\) rad relative to odom

Since:

\[
\pi = 180^\circ
\]

the robot front points toward:

\[
-x_{odom}
\]

A transform answers:

> Where is this frame relative to another frame?

---

## 6. Robot Forward Depends on Orientation

Example:

Robot pose:

\[
(2,3,\pi/2)
\]

Since:

\[
\pi/2=90^\circ
\]

the robot's `+x_base` direction points toward:

\[
+y_{odom}
\]

If the robot moves forward 1.5 m:

\[
x=2
\]

stays unchanged.

\[
y=3+1.5=4.5
\]

So:

\[
(2,4.5,\pi/2)
\]

This showed that:

> `+x_base` can point toward `+y_odom`.

---

## 7. Negative Orientation

Example:

\[
\theta=-\pi/2
\]

means:

\[
-90^\circ
\]

which points toward:

\[
-y_{odom}
\]

It does NOT mean the robot is moving backward.

Orientation and velocity are different.

A robot can face:

\[
-\pi/2
\]

and still move forward relative to its own front.

---

## 8. Equivalent Angles

Different angle values can represent the same physical orientation.

Example:

\[
-\pi/2
\]

and:

\[
3\pi/2
\]

both represent the same direction.

Because:

\[
-\pi/2=-90^\circ
\]

and:

\[
3\pi/2=270^\circ
\]

Both point toward:

\[
-y
\]

---

## 9. Degrees to Radians

ROS and robotics equations normally use radians.

Conversion:

\[
\theta_{rad}
=
\theta_{deg}\frac{\pi}{180}
\]

Examples learned today:

\[
30^\circ=\pi/6
\]

\[
60^\circ=\pi/3
\]

\[
90^\circ=\pi/2
\]

\[
120^\circ=2\pi/3
\]

\[
150^\circ=5\pi/6
\]

\[
180^\circ=\pi
\]

\[
210^\circ=7\pi/6
\]

\[
270^\circ=3\pi/2
\]

\[
300^\circ=5\pi/3
\]

\[
330^\circ=11\pi/6
\]

\[
360^\circ=2\pi
\]

Important method:

\[
degrees\times\frac{\pi}{180}
\]

Then simplify the fraction.

I should not depend only on memorization.

---

## 10. Robot Motion at Non-Axis Angles

If the robot faces exactly:

- 0°
- 90°
- 180°
- 270°

it is easy to reason about x and y.

But real robots can face:

\[
30^\circ,\ 45^\circ,\ 60^\circ,\ 0.7rad
\]

etc.

Therefore we need sine and cosine.

For straight robot movement:

\[
\Delta x=\Delta s\cos(\theta)
\]

\[
\Delta y=\Delta s\sin(\theta)
\]

Physical meaning:

> cosine tells how much robot-forward movement goes into the odom x direction.

> sine tells how much robot-forward movement goes into the odom y direction.

---

## 11. 45-Degree Example

For:

\[
\Delta s=2m
\]

and:

\[
\theta=45^\circ
\]

\[
\cos45^\circ\approx0.707
\]

\[
\sin45^\circ\approx0.707
\]

Therefore:

\[
\Delta x\approx1.414m
\]

\[
\Delta y\approx1.414m
\]

Important correction:

A 2 m diagonal movement does NOT mean:

\[
1m\text{ in x}+1m\text{ in y}
\]

The x and y values are components of the same 2 m movement.

---

## 12. 30-Degree Example

For:

\[
\Delta s=2m
\]

and:

\[
\theta=30^\circ
\]

\[
\cos30^\circ\approx0.866
\]

\[
\sin30^\circ=0.5
\]

Therefore:

\[
\Delta x\approx1.732m
\]

\[
\Delta y=1m
\]

If starting at:

\[
(x,y)=(2,2)
\]

the pose becomes:

\[
(3.732,3,\pi/6)
\]

The sketch is useful to predict direction, but sine and cosine give the exact values.

---

## 13. 60-Degree Example

For:

\[
\theta=60^\circ=\pi/3
\]

and:

\[
\Delta s=2m
\]

the correct components are:

\[
\Delta x=1m
\]

\[
\Delta y\approx1.732m
\]

I initially swapped x and y.

A useful physical check:

60° is closer to the +y axis than the +x axis.

Therefore:

\[
\Delta y>\Delta x
\]

This kind of reasoning can help detect calculation mistakes.

---

## 14. Engineering Method

For robot movement at an arbitrary orientation:

1. Look at the robot orientation \(\theta\).
2. Sketch the approximate direction.
3. Predict whether x and y should increase or decrease.
4. Calculate:

\[
\Delta x=\Delta s\cos\theta
\]

\[
\Delta y=\Delta s\sin\theta
\]

5. Update:

\[
x_{new}=x_{old}+\Delta x
\]

\[
y_{new}=y_{old}+\Delta y
\]

6. If the robot did not rotate:

\[
\theta_{new}=\theta_{old}
\]

The drawing gives intuition.

The mathematics gives precision.

---

## Learning Evidence

Today I was able to reason about:

- `base_link`
- `odom`
- `map`
- `map → odom → base_link`
- why odometry must stay smooth
- what a TF transform represents
- movement relative to different frames
- positive and negative orientations
- equivalent angle representations
- converting degrees to radians
- using sine and cosine to project robot-forward movement into odom x/y movement

I also worked through several pose examples manually in my notebook.

The main conceptual improvement today was understanding that:

> The robot always moves forward along its own `+x_base`, while odometry must calculate how that movement affects the fixed `odom` x and y coordinates.

## Current Understanding

I understand the frame concept better now.

My current weak points are:

- quickly converting unfamiliar angles between degrees and radians
- remembering which component uses cosine and which uses sine
- interpreting non-axis orientations such as 30°, 45°, and 60°

These need more practice before moving deeper into odometry implementation.

## Next Session

Continue from:

\[
(x,y,\theta)=(2,2,\pi/3)
\]

with:

\[
\Delta s=2m
\]

We already found:

\[
\Delta x=1m
\]

\[
\Delta y\approx1.732m
\]

Next session:

- complete the pose update
- practice arbitrary-angle motion
- strengthen sine/cosine physical meaning
- then reconnect this to differential-drive wheel encoder odometry
