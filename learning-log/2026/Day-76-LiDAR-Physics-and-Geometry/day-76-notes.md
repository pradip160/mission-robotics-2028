# Mission World 2028 — Day 76 Learning Log

**Date:** Tuesday, 3 November 2026  
**Project:** ROS 2 Restaurant Delivery Robot  
**Session:** 2D LiDAR — physics, geometry, and first handwritten exercises    
**Status:** Initial physics and geometry checkpoint completed; next geometry exercise deferred to the next study session  
**Previous log:** Days 73–75 — trajectory safety and transition to embodied robotics

## 1. Why I Returned to the Restaurant Robot

I decided to focus my practical learning on the existing restaurant delivery robot as a foundation for **embodied robotics research**. My long-term ambition includes safe, adaptable robots working in unfamiliar restaurant and kitchen environments and, eventually, manipulation and cooking robots. The near-term technical goal is smaller and testable: give my existing mobile robot real simulated sensor measurements, learn to interpret them, and eventually use them for mapping and localisation.

I clarified my study preference: **depth rather than speed**. I do not want to move on merely because a topic has been covered or a program runs. The agreed study sequence is:

**Theory → Physical meaning → Mathematics → Small implementation → Testing → Debugging → Independent verification.**

This session focused on understanding LiDAR *before* making ROS 2 or Gazebo changes.

## 2. Existing Project Baseline

My ROS 2 Jazzy repository already contains:

- `restaurant_robot_status`: nodes for sensor-status messages, navigation logic, safety/recovery, and odometry.
- `restaurant_robot_description`: URDF robot geometry and a Gazebo world.
- `restaurant_robot_interfaces`: custom message definitions.
- An odometry node that publishes `/odom` and broadcasts `odom -> base_link`.

**Important limitation of the current project:** The checked `lidar_obstacle_publisher.py` publishes predefined obstacle-status/distance values, not a real `sensor_msgs/msg/LaserScan` stream from a Gazebo LiDAR. The URDF version reviewed did not contain a LiDAR sensor definition. These are the next integration tasks; they were **not** completed today.

## 3. Physics: How Time-of-Flight LiDAR Measures Distance

For a simplified pulsed **time-of-flight** LiDAR, emitted light travels from the sensor to a reflecting object and back. Because the measured time is the *round-trip* time,

$$
\boxed{d=\frac{ct}{2}}
$$

where:

- $d$ is one-way distance to the object, in metres;
- $c\approx3.0\times10^8\ \mathrm{m/s}$ is the approximate speed of light in air;
- $t$ is the measured round-trip time, in seconds.

Not every real LiDAR uses pulsed time of flight; other ranging techniques exist. The equation is the physics model used in today's lesson.

### Exercise A — Wall 4 m from the LiDAR

Given $d=4\ \mathrm{m}$:

- One-way travel distance: $4\ \mathrm{m}$.
- Round-trip travel distance: $2d=8\ \mathrm{m}$.
- One-way travel time:

$$
t_{\mathrm{one\ way}}=\frac{4}{3\times10^8}
\approx1.333\times10^{-8}\ \mathrm{s}
=13.33\ \mathrm{ns}.
$$

- Round-trip travel time:

$$
t_{\mathrm{round\ trip}}=\frac{8}{3\times10^8}
\approx2.667\times10^{-8}\ \mathrm{s}
=\boxed{26.67\ \mathrm{ns}}.
$$

**My explanation:** The pulse must travel 4 m to reach the wall, then another 4 m to return to the sensor. I correctly distinguished one-way and round-trip measurements. A minor notation correction was to avoid calling the 4 m one-way distance `d_total`.

## 4. Geometry: Polar to Cartesian Coordinates

A 2D laser scan provides range $r$ along a measurement beam and the beam angle $\theta$ relative to the sensor frame. It does not directly output global object coordinates.

Coordinate convention for the lesson:

- $+x$: forward from the LiDAR;
- $+y$: to the left;
- positive angles: counterclockwise as viewed from above;
- negative angles: clockwise / to the right.

Polar-to-Cartesian conversion:

$$
\boxed{x=r\cos\theta},\qquad
\boxed{y=r\sin\theta}.
$$

The measured point is expressed **relative to the LiDAR frame**, not necessarily relative to `base_link`, `odom`, or `map`.

### Exercise B — Range 5 m, angle +60°

$$
x=5\cos60^\circ=5(0.5)=\boxed{2.50\ \mathrm{m}}
$$

$$
y=5\sin60^\circ=5(0.8660)\approx\boxed{4.33\ \mathrm{m}}
$$

Thus:

$$
\boxed{P=(2.50,\ 4.33)\ \mathrm{m}}.
$$

**Interpretation:** The measured point is 2.50 m forward and approximately 4.33 m left of the LiDAR. These are components of the 5 m range, not two separate range measurements.

### Exercise C — Range 3 m, angle −30°

$$
x=3\cos(-30^\circ)=3(0.8660)\approx\boxed{2.598\ \mathrm{m}}
$$

$$
y=3\sin(-30^\circ)=3(-0.5)=\boxed{-1.50\ \mathrm{m}}
$$

Thus:

$$
\boxed{P=(2.598,\ -1.50)\ \mathrm{m}}.
$$

**Interpretation:** The point is forward and to the **right** of the LiDAR. The negative $y$ indicates direction, not a negative physical range.

### Independent sanity-check method

Recover the range from Cartesian coordinates:

$$
r=\sqrt{x^2+y^2}.
$$

For the earlier worked example $r=2\ \mathrm{m}$ and $\theta=30^\circ$, I had noted $P\approx(1.732,1.0)\ \mathrm{m}$ and checked that $\sqrt{1.732^2+1^2}\approx2\ \mathrm{m}$.

**Practical reminder:** Check calculator degree/radian settings. When later working with ROS 2, angles are ordinarily represented in radians.

## 5. What One Scan Really Represents

A single range alone does not determine the location of a measured point; the beam direction is also needed. Several beams may have identical ranges but different positions in the plane.

A full 2D scan consists of many range readings associated with successive angles. In the simple model, each valid beam can be converted into a Cartesian point:

$$
(x_i,y_i)=(r_i\cos\theta_i,\ r_i\sin\theta_i).
$$

**Important limits, introduced but not yet examined experimentally:**

- The scan samples a plane, not the full 3D scene.
- Narrow obstacles may fall between neighbouring beams.
- Glass, shiny surfaces, dark surfaces, range limits, and environmental conditions can cause problematic or missing returns.
- An invalid reading **must not automatically be interpreted as a clear path**.
- Measurements are sensor-relative. Mapping them into a global frame requires the LiDAR mounting transform, robot pose estimate, and appropriate timestamps.

## 6. Learning Evidence and Supervisor Feedback

**Evidence:** I submitted two handwritten notebook pages showing all three exercise calculations, unit conversions, negative-angle signs, and some self-corrections.

**Demonstrated in today's exercises:**

- Correct round-trip time-of-flight calculation: 26.67 ns for a 4 m wall.
- Correct polar-to-Cartesian conversion at +60°: $(2.50,4.33)$ m.
- Correct conversion at −30°: $(2.598,-1.50)$ m.
- Correct physical reasoning for the doubled travel distance.
- Ability to use Pythagoras to sanity-check a range from coordinate components.

**Still to establish:**

- Ability to interpret a complete scan rather than one beam.
- Angular resolution and finite obstacle visibility.
- Sensor noise, invalid returns and uncertainty propagation.
- Frame transformations using a moving robot and a mounted sensor.
- Direct implementation, visualisation, calibration and testing of an actual simulated LiDAR.

**Not completed or claimed:** No new code, URDF sensor modification, Gazebo sensor run, `/scan` publication, RViz visualisation, automated test, or SLAM map was reported in this lesson.

## 7. Exact Stopping Point — Resume Here Next Session

The final short exercise was assigned but **not yet answered**:

Two laser measurements are:

$$
P_1=(r=3\ \mathrm{m},\ \theta=0^\circ)
$$

$$
P_2=(r=3\ \mathrm{m},\ \theta=90^\circ)
$$

**Next actions:**

1. Calculate Cartesian coordinates of $P_1$ and $P_2$.
2. Explain each point's position relative to the robot/LiDAR.
3. Begin the next deep lesson: **field of view, angular resolution and laser-scan geometry**. Derive the number of beams for an inclusive scan interval and distinguish angular spacing from range accuracy.
4. Investigate why thin obstacles can be missed at greater distances; use $s\approx r\Delta\theta$ with $\Delta\theta$ in radians.
5. Only after understanding and validating scan geometry, proceed toward actual simulated LiDAR integration in Gazebo and ROS 2.

## 8. Session Reflection

I want to build robotics expertise through genuine understanding, implementation, and repeatable experiments, not by rushing through topic lists or relying entirely on hypothetical Q&A. Today's handwritten work provides evidence of the first mathematical foundation. Next, I will connect individual measurements into the geometry of a full scan before writing ROS 2 code.

**Mission World 2028 research direction:** Embodied robotics, starting from a reliable, adaptable restaurant mobile robot and eventually expanding to manipulation and kitchen robotics. The immediate work remains a foundation for pursuing a funded, research-focused Master's with strong laboratory access and supervision.

---

**Session status:** Pause here for rest. Resume from the two-point exercise. Do not mark full LiDAR mastery or sensor integration as complete.
