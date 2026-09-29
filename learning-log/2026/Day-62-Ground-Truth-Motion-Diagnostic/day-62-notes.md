Day 62 — Ground-Truth Motion Diagnostic and Wheel-Contact Calibration
Date: 2026-09-29
Project: ROS2 Restaurant Delivery Robot
Focus: Curved-motion odometry error, Gazebo ground-truth measurement, wheel-contact calibration
Goal
Investigate why the robot had very small straight-line odometry error but larger curved-motion error.
The main question was:
Is the curved error caused by lateral slip, wrong wheel geometry, speed, or Gazebo contact physics?

Ground-Truth Diagnostic
A separate diagnostic node was used so odometry_node.py stayed unchanged.
The diagnostic reads raw Gazebo physics ground truth from:
/world/restaurant_world/dynamic_pose/info
Run with:
gz topic -e \
-t /world/restaurant_world/dynamic_pose/info \
--json-output | python3 ground_truth_motion_diagnostic.py
The node calculates:
- robot world position: x, y
- yaw: theta
- change in yaw: delta_theta
- forward displacement in the robot frame
- sideways displacement in the robot frame
- forward velocity
- sideways velocity
- angular velocity
The body-frame equations are:
forward =
    delta_x * cos(theta_mid)
    + delta_y * sin(theta_mid)

sideways =
    -delta_x * sin(theta_mid)
    + delta_y * cos(theta_mid)
where:
theta_mid = previous_theta + delta_theta / 2
Yaw difference is wrapped safely using:
delta_theta = math.atan2(
    math.sin(theta - previous_theta),
    math.cos(theta - previous_theta)
)
Timestamp Bug Found
Gazebo timestamps contain:
sec
nsec
The correct time is:
current_time = (
    float(stamp["sec"])
    + float(stamp.get("nsec", 0)) * 1e-9
)
Using only sec caused delta_t to be about one second and produced incorrect velocity values.
Using:
stamp["nsec"]
sometimes caused:
KeyError: 'nsec'
because Gazebo may omit nsec when its value is zero.
The robust fix is:
stamp.get("nsec", 0)
Original Curved-Motion Finding
For:
linear.x  = 0.20 m/s
angular.z = 0.20 rad/s
with the original drive-wheel collision width of about 0.05 m:
odometry angular velocity ≈ 0.20 rad/s
Gazebo actual angular velocity ≈ 0.1846 rad/s
The robot physically rotated more slowly than the wheel-based differential-drive model predicted.
The error was approximately:
7.69% low
Forward velocity was almost exactly correct and sideways velocity was extremely small.
This showed that lateral sideways slip was not the main cause.
Wheel Speeds
Measured JointState wheel velocities during the 0.20 / 0.20 curve:
left_wheel_joint  ≈ 1.4 rad/s
right_wheel_joint ≈ 2.6 rad/s
With wheel radius:
r = 0.10 m
wheel linear velocities are:
v_left  = 0.14 m/s
v_right = 0.26 m/s
Ideal differential-drive angular velocity with:
wheel_separation = 0.60 m
is:
omega = (0.26 - 0.14) / 0.60
      = 0.20 rad/s
So the encoder/odometry side was behaving as expected.
Drive-Wheel Collision-Width Experiment
Only the physical collision width of the drive wheels was changed.
The visual wheel width stayed unchanged.
The experiment showed that changing collision/contact geometry changed the physical turning behaviour in Gazebo.
A collision width of:
0.035 m
gave the best angular-rate match in the controlled tests after fixing the timestamp code.
0.035 m Collision Width — Fast Curve
Command:
linear.x  = 0.20 m/s
angular.z = 0.20 rad/s
Measured Gazebo motion:
v_forward  ≈ 0.2034 m/s
v_sideways ≈ -0.0000203 m/s
omega      ≈ 0.2000 rad/s
Angular velocity matched the target almost perfectly.
However, forward velocity was about:
1.7% high
0.035 m Collision Width — Slow Curve
Command:
linear.x  = 0.10 m/s
angular.z = 0.10 rad/s
Measured:
v_forward  ≈ 0.10175 m/s
v_sideways ≈ -0.000005 m/s
omega      ≈ 0.1000 rad/s
Again:
- angular velocity matched
- sideways motion was negligible
- forward velocity was about 1.75% high
This showed that the angular calibration generalized from 0.20 / 0.20 to 0.10 / 0.10.
Straight-Motion Tests
Slow straight
Command:
linear.x  = 0.10
angular.z = 0.00
Measured:
v_forward ≈ 0.100000 m/s
omega     ≈ 0
sideways  ≈ 0
Fast straight
Command:
linear.x  = 0.20
angular.z = 0.00
Measured:
v_forward ≈ 0.200000 m/s
omega     ≈ 0
sideways  ≈ 0
This ruled out a general wheel-radius error and ruled out speed alone as the cause.
Straight motion is extremely accurate.
Gentler Turning Test
Command:
linear.x  = 0.20
angular.z = 0.10
Measured:
v_forward  ≈ 0.20175 m/s
v_sideways ≈ -0.000010 m/s
omega      ≈ 0.1000 rad/s
Forward error:
≈ 0.875% high
Comparison:
0.20 / 0.00 → forward error ≈ 0%
0.20 / 0.10 → forward error ≈ 0.88%
0.20 / 0.20 → forward error ≈ 1.70%
The remaining forward-motion error increases as angular velocity increases.
A useful empirical pattern is:
extra forward velocity ≈ 0.017 * omega
approximately for these tests.
Current Interpretation
The evidence currently supports:
1. Straight-line motion is accurate.
2. Wheel encoder values are correct.
3. Lateral sideways motion is negligible.
4. The original curved-motion problem was mainly a physical turning-rate mismatch in Gazebo.
5. Changing drive-wheel collision/contact width changes the physical turning behaviour.
6. 0.035 m collision width gives a very good angular-rate match for the tested curves.
7. A smaller residual forward-speed increase remains only during turning.
8. This residual effect appears coupled to angular velocity rather than speed alone.
9. The remaining cause has not yet been fully identified.
The next likely question is whether the remaining effect is related to:
- drive-wheel axle position
- robot/base reference-point location
- contact geometry
- the point whose pose is being measured
Important Experimental Lesson
Do not randomly tune parameters.
The useful workflow was:
observe error
→ form hypothesis
→ change one variable
→ measure ground truth
→ compare prediction vs physics
→ reject or support the hypothesis
This investigation separated:
straight-motion accuracy
turning-rate error
lateral slip
speed effects
contact-width effects
turning/forward coupling
instead of treating all odometry drift as one problem.
Current Simulation Setting
Drive-wheel collision width:
<length>0.035</length>
for both:
left_wheel_collision
right_wheel_collision
Do not change this before continuing the next investigation.
Next Session
Continue from:
Why does forward velocity become slightly higher only while the robot is turning?

First inspect:
drive-wheel axle position
restaurant_robot/base_link origin
ground-truth reference point
Then determine whether the remaining forward increase is a reference-point geometry effect or a contact/physics effect.
Learning Evidence
Today I:
- built and used a Gazebo ground-truth motion diagnostic
- converted world-frame motion into robot-frame forward and sideways motion
- used Gazebo timestamps to calculate real velocities
- fixed a timestamp nsec bug
- compared wheel-predicted motion against physics ground truth
- showed that lateral slip was negligible
- identified a turning-rate mismatch in curved motion
- tested drive-wheel collision width as a controlled variable
- found that 0.035 m produced accurate angular velocity in the tested curves
- verified that straight motion remained accurate at both 0.10 m/s and 0.20 m/s
- found a remaining forward-motion error that increases with turning rate
Resume Point
Validated custom differential-drive odometry against raw Gazebo physics ground truth. Built a body-frame motion diagnostic using pose and timestamp data, isolated curved-motion error from lateral slip and straight-line scale error, and experimentally showed that drive-wheel contact geometry affects physical angular velocity. Calibrated the simulation to achieve near-exact angular-rate tracking across multiple curved-motion speeds and identified a remaining turning-dependent forward-motion coupling for further investigation.
