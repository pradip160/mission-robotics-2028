# Day 64 — SLAM Foundations, Loop Closure, Frames and TF Composition

## Mission Korea 2028

Today I continued from my completed odometry and physical-model calibration work and started building a deeper understanding of SLAM.

The main goal was not to run a SLAM package yet.

The goal was to understand:

- Why SLAM is needed
- How odometry drift affects mapping
- Local scan matching
- Loop closure
- Why SLAM may correct old poses
- Why ROS uses both `map` and `odom`
- The TF chain `map -> odom -> base_link`
- Why 2D transform composition is more complicated than simple subtraction

---

# 1. Why SLAM Is Needed

Wheel odometry estimates the robot pose:

\[
(x, y, \theta)
\]

by integrating wheel motion over time.

Odometry is useful because it provides smooth local motion estimates.

However, odometry is not globally accurate forever.

Errors can come from:

- wheel slip
- wheel-radius error
- wheel-separation error
- encoder noise
- imperfect physical modelling
- contact effects

These errors accumulate.

For example:

```text
Actual robot position = 1.8 m
Odometry estimate     = 2.0 m

Odometry has overestimated the motion by:
0.2 m

If the robot continues using only odometry, this error can grow.
2. What SLAM Means
SLAM:
Simultaneous Localization And Mapping

The robot tries to solve two related problems:
Localization:
Where am I?

Mapping:
What does the environment around me look like?

These problems depend on each other.
To place a LiDAR measurement correctly in a map, the robot needs a good estimate of its pose.
But the robot can also use the environment/map to improve its pose estimate.
Therefore SLAM continuously connects:
robot motion
+
sensor observations
+
pose estimation
+
mapping

3. Accurate LiDAR Does Not Automatically Mean an Accurate Map
A very important concept I learned:
\[
\boxed{
\text{accurate sensor measurement}
+
\text{wrong robot pose}
=
\text{wrong map}
}
\]
Example:
The LiDAR correctly measures:
Wall = 2 m in front of robot

But suppose the robot's estimated pose is wrong.
SLAM must transform the LiDAR measurement from the robot frame into the global map frame.
If the robot pose is wrong, SLAM can place the correctly measured wall at the wrong global location.
Therefore sensor accuracy alone is not enough.
The pose used to transform the measurement is also extremely important.
4. Orientation Error Can Distort the Whole Environment
Suppose:
Actual orientation    = 0 degrees
Estimated orientation = 10 degrees

The LiDAR can still correctly measure distances.
However, when those measurements are transformed into the map using the wrong orientation, the scan can be rotated.
A straight wall may appear:
- angled
- shifted
- duplicated
- inconsistent with an earlier scan
This taught me that orientation error can become especially dangerous because it affects many environmental measurements at once.
It can look as if the whole environment has rotated relative to the robot.
5. Building a Map Using Drifted Poses
If the robot continues mapping while its pose is drifting, the map can become distorted.
Even if every LiDAR range measurement is accurate, incorrect pose estimates cause those measurements to be inserted into incorrect global locations.
My analogy was:
If I want to travel to Central London but the map incorrectly places the destination toward Greenwich, I may follow the map correctly but still travel in the wrong direction.
The robot has a similar problem.
Correct sensor measurements are not enough if the coordinate system/map they are placed into is wrong.
6. Local Scan Matching
SLAM does not wait until the robot returns to its starting location before making corrections.
While moving, the robot can compare:
current LiDAR scan
        ↕
recent scan / nearby local map

This can help estimate small pose corrections continuously.
This is generally called:
local scan matching

or part of:
local SLAM / local tracking

Example:
scan at t = 10.0 s

compared with

scan at t = 10.1 s

The scans are temporally close and represent nearby parts of the environment.
This is NOT loop closure.
7. Loop Closure
Loop closure happens when the robot recognizes a location that it visited much earlier.
Example:
Robot starts near kitchen entrance.

Robot explores restaurant for 10 minutes.

Odometry slowly drifts.

Robot eventually returns near the same kitchen entrance.

LiDAR recognizes:
- same wall
- same doorway
- same corner
- same counter

SLAM realizes:
"I have been here before."

This is:
\[
\boxed{\text{Loop Closure}}
\]
Loop closure creates a constraint between the current pose and an old pose.
Conceptually:
pose -- pose -- pose -- pose -- pose
 |                             |
 +-------- loop closure -------+

The loop closure says that two poses that the trajectory believed were far apart should actually represent approximately the same physical location.
8. Why Correcting Only the Current Pose Is Not Enough
Odometry drift accumulates gradually.
Suppose the robot has poses:
\[
P_1, P_2, P_3, ..., P_{100}
\]
Small errors happen during many motion updates.
By pose \(P_{100}\), the total error may be:
0.5 m

The full error was not created only at pose 100.
It accumulated through the trajectory.
Therefore when loop closure detects a contradiction, SLAM may need to adjust multiple earlier pose estimates.
This can improve:
- trajectory consistency
- wall alignment
- map consistency
- future localization
This introduces the idea of:
Pose Graph Optimization

I have not studied pose-graph mathematics deeply yet.
For now my understanding is:
poses = nodes

motion / observations / loop closures = constraints or edges

SLAM tries to find poses that satisfy these constraints as consistently as possible.
9. Local Scan Matching vs Loop Closure
These two corrections are related but different.
Local scan matching
Usually compares:
current observation
with
recent observation / local map

It helps maintain accurate short-term tracking.
Example:
10.0 seconds -> 10.1 seconds

Loop closure
Compares:
current place
with
a place seen much earlier

Example:
10 seconds -> 600 seconds

Loop closure is especially useful for correcting long-term accumulated drift.
Therefore:
SLAM
=
local tracking
+
mapping
+
loop closure
+
global correction

Loop closure is an important component of many SLAM systems, not a completely separate SLAM method.
10. Why ROS Has Both map and odom
This was initially confusing.
The main TF chain is:
map
 |
 v
odom
 |
 v
base_link

or:
map -> odom -> base_link

Each transform has a different responsibility.
11. odom -> base_link
This represents the robot's smooth local motion estimate.
For example:
0.0
0.1
0.2
0.3
0.4
...

Wheel odometry normally provides this relationship.
Important:
odom does NOT mean globally correct.

Odometry can drift.
Its important property is that it is normally:
smooth
and
locally continuous

This is useful for robot control.
12. map -> odom
SLAM provides the relationship between the globally corrected map frame and the drifting odom frame.
Instead of suddenly changing:
odom -> base_link

SLAM can change:
map -> odom

This allows local odometry to stay smooth while the global robot pose is corrected.
Therefore:
odom -> base_link

is mainly associated with local smooth motion.
And:
map -> odom

contains the global SLAM correction.
13. map -> base_link
The globally corrected robot pose can be obtained by composing:
map -> odom

with:
odom -> base_link

So:
\[
\boxed{
T_{map,base}
=
T_{map,odom}
T_{odom,base}
}
\]
Conceptually:
map
 ↓
global SLAM correction
 ↓
odom
 ↓
local odometry
 ↓
base_link

14. Why SLAM Does Not Simply Rewrite Odometry
Suppose odometry says:
x = 5.0 m

SLAM discovers through loop closure that globally the robot should be:
x = 4.5 m

It would be undesirable for local odometry to suddenly jump:
5.0 -> 4.5

because the physical robot did not teleport backwards by 0.5 m.
A controller using that pose could suddenly see a large error and produce an abrupt command.
So SLAM can preserve the smooth local odometry and instead correct the relationship:
map -> odom

15. Simple 1D map -> odom Examples
For simple 1D examples with no rotation:
\[
\text{map pose}
=
\text{map -> odom}
+
\text{odom pose}
\]
Therefore:
\[
\boxed{
\text{map -> odom}
=
\text{map pose}
-
\text{odom pose}
}
\]
Example 1:
odom = 4.0 m
map  = 3.6 m

Then:
\[
3.6 - 4.0 = -0.4
\]
Therefore:
map -> odom = -0.4 m

Check:
\[
-0.4 + 4.0 = 3.6
\]
Example 2:
odom = 5.0 m
map  = 5.3 m

Then:
\[
5.3 - 5.0 = +0.3
\]
Therefore:
map -> odom = +0.3 m

Check:
\[
5.0 + 0.3 = 5.3
\]
Example 3:
odom = 6.2 m
map  = 5.7 m

Then:
\[
5.7 - 6.2 = -0.5
\]
Therefore:
map -> odom = -0.5 m

Check:
\[
6.2 - 0.5 = 5.7
\]
16. Important Lesson About Signs
I initially understood the size of the disagreement but sometimes reversed the sign.
The safe rule for the simple 1D case is:
\[
\boxed{
\text{correction}
=
\text{desired global value}
-
\text{odom value}
}
\]
Do not guess whether the correction is positive or negative.
Calculate it.
17. Moving from 1D to 2D
A real mobile robot has:
\[
(x,y,\theta)
\]
Therefore map -> odom may contain corrections in:
x
y
theta

Example:
Odometry:
\[
(x,y,\theta)
=
(5.0,1.0,30^\circ)
\]
SLAM:
\[
(x,y,\theta)
=
(4.6,1.3,25^\circ)
\]
This tells us conceptually:
odom x     = too high
odom y     = too low
odom theta = too high

However, 2D transforms are more complicated than doing three independent subtractions.
Why?
Because rotation changes how translation must be interpreted.
18. Coordinates Only Make Sense Relative to a Frame
An important concept:
x and y are not absolute by themselves.

They are coordinates expressed relative to a particular coordinate frame.
For example:
(1,0) in odom

means:
1 metre along odom's +x axis

It does NOT automatically mean:
1 metre along map's +x axis

because the odom frame itself may be rotated relative to the map frame.
19. Concrete Transform Example
Suppose:
map -> odom

has:
translation:
x = 1 m
y = 2 m

rotation:
theta = 90 degrees

This means:
The odom origin is located at (1,2) in the map.

The odom axes are rotated 90 degrees relative to the map axes.

Now suppose:
odom -> base_link

says:
x = 1 m
y = 0 m

This means the robot is:
1 metre along the ODOM x-axis.

But because odom is rotated by 90 degrees:
odom +x

points along:
map +y

Therefore the local displacement:
(1,0)

in odom becomes:
(0,1)

when expressed in map coordinates.
Then add the position of the odom origin:
odom origin in map = (1,2)

robot displacement = (0,1)

Therefore:
\[
(1,2)+(0,1)=(1,3)
\]
So:
map -> base_link position = (1,3)

20. Orientation Composition
In the same example:
map -> odom orientation = 90 degrees

odom -> base_link orientation = 30 degrees

Then the robot's global orientation is:
\[
90^\circ + 30^\circ
=
120^\circ
\]
Therefore:
\[
\boxed{
map -> base\_link
=
(x=1,\ y=3,\ \theta=120^\circ)
}
\]
21. 2D Transform Equation
The general position equation introduced today was:
\[
\boxed{
t_{map,base}
=
t_{map,odom}
+
R_{map,odom}t_{odom,base}
}
\]
The rotation matrix is:
\[
R(\theta)
=
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
\]
Physical meaning:
Global robot position
=
global position of odom origin
+
robot's local displacement rotated into the global/map axes

This physical sentence is currently more important for me than memorizing the equation.
22. Why Rotation Happens Before Translation Addition
Suppose:
map -> odom = (1,2,90 degrees)

odom -> base_link = (1,0)

The (1,0) is expressed using odom axes.
Before adding it to the global map position, it must first be expressed using map axes.
Because odom is rotated 90 degrees:
odom (1,0)

becomes:
map (0,1)

Then:
(1,2) + (0,1) = (1,3)

Therefore the sequence is conceptually:
local robot displacement
        ↓
rotate into map axes
        ↓
add global position of odom origin
        ↓
global robot position

23. Current Understanding
Concepts I now understand reasonably well:
- why odometry drift occurs
- why SLAM is needed
- why accurate LiDAR can still create a bad map if pose is wrong
- why orientation error can distort map observations
- local scan matching vs loop closure
- why loop closure can affect previous poses
- basic pose-graph idea
- purpose of map
- purpose of odom
- purpose of base_link
- why odom -> base_link should remain smooth
- why SLAM normally corrects map -> odom
- simple 1D map -> odom correction
- positive and negative correction concept
- coordinates depend on reference frames
24. Concepts Not Yet Fully Comfortable
I am NOT yet fully confident with:
- 2D transform composition
- mentally converting coordinates between rotated frames
- rotation matrices
- calculating map -> base_link when both translation and rotation exist
- full TF mathematics
- computing an inverse transform
- pose graph optimization mathematics
This is the exact point where I stopped.
I should not rush past this.
25. Next Study Checkpoint
Continue from:
map -> odom = (2,1,90 degrees)

This means:
odom origin is at map position (2,1)

odom +x points along map +y

Robot position relative to odom:
odom -> base_link = (2,0)

Meaning:
robot is 2 metres along odom +x

Next task:
Work out where the robot should be in the map frame WITHOUT using matrix multiplication first.
The goal is to understand the physical frame relationship before doing more mathematics.
26. Important Mental Model
Keep this TF tree in mind:
map
 |
 | SLAM global correction
 v
odom
 |
 | smooth local wheel odometry
 v
base_link

And remember:
odom -> base_link

answers:
"Where is my robot relative to odom?"

while:
map -> odom

answers:
"Where is the odom coordinate system relative to the global map?"

Combining them lets us answer:
"Where is the robot in the global map?"

Learning Evidence
During this study I was able to explain in my own words that:
- a map built using drifted poses becomes incorrect even if sensors measure correctly
- orientation error can make the environment appear rotated
- loop closure happens when the robot recognizes a previously visited location
- local scan matching is different from loop closure
- SLAM should preserve smooth odometry and maintain a separate global correction
- map -> odom describes the disagreement/correction between global SLAM and local odometry
- in simple 1D examples I can calculate the correction sign and magnitude
- in 2D, frame rotation changes how local x/y motion appears in the global frame
I am currently still developing intuition for 2D transform composition and should continue from this point before moving deeper into SLAM implementation.
Research Thinking
The major lesson from this stage is that robotics estimation is not simply about obtaining sensor measurements.
Every measurement exists relative to a coordinate frame.
To build a consistent map, the robot must understand:
what was measured
+
from which pose
+
in which frame
+
how that frame relates to other frames

A sensor measurement can be accurate while the resulting global estimate is wrong because the pose or transform used to interpret that measurement is wrong.
This is directly relevant to SLAM, localization, sensor fusion, navigation, and autonomous mobile robots.


