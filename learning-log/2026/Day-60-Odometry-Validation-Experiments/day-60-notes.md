# Day 60 – Odometry Validation and Repeatability Experiments

Date: 24 September 2026

## Goal

After completing my custom differential-drive odometry implementation, the next goal was to stop asking only:

> "Does my odometry work?"

and start asking:

> "How accurate is my odometry, when does the error appear, and is that error repeatable?"

This checkpoint covers the practical validation work completed after Day 59.

The main experiment compares:

```text
Custom Wheel Odometry
        vs
Gazebo Ground Truth
```

The focus was on:

- clean straight-line motion
- curved motion
- repeated trials
- position error
- heading error
- systematic vs random error
- experimental control
- identifying the next variables to investigate

---

# 1. Experimental Architecture

The comparison pipeline is:

```text
Gazebo Physics
    │
    ├── Ground-Truth Robot Pose
    │
    └── Wheel Joint States
             ↓
        ros_gz_bridge
             ↓
    sensor_msgs/JointState
             ↓
      odometry_node.py
             ↓
       Custom /odom
```

This gives two independent pose sources:

```text
Custom odometry:
x_odom
y_odom
theta_odom

Gazebo:
x_true
y_true
theta_true
```

The custom odometry uses wheel motion.

Gazebo ground truth comes from the simulator's physics state.

---

# 2. Simulation Setup

## Start Gazebo

```bash
gz sim ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_description/worlds/restaurant_world.sdf
```

---

## Spawn Robot

```bash
gz service -s /world/restaurant_world/create \
--reqtype gz.msgs.EntityFactory \
--reptype gz.msgs.Boolean \
--timeout 15000 \
--req 'sdf_filename: "/home/pradip/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_description/models/restaurant_robot.sdf", name: "restaurant_robot", pose: {position: {x: 0, y: 0, z: 0.5}}'
```

Successful spawn:

```text
data: true
```

---

## Start JointState Bridge

```bash
source /opt/ros/jazzy/setup.bash

ros2 run ros_gz_bridge parameter_bridge \
'/world/restaurant_world/model/restaurant_robot/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'
```

---

## Run Custom Odometry Node

```bash
source /opt/ros/jazzy/setup.bash

cd ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_status/restaurant_robot_status

python3 odometry_node.py
```

---

## Custom Odometry Measurement

```bash
ros2 topic echo /odom --once
```

---

## Gazebo Ground Truth

```bash
gz topic -e -t /world/restaurant_world/dynamic_pose/info
```

The important entry is:

```text
name: "restaurant_robot"
```

I record:

```text
position.x
position.y

orientation.x
orientation.y
orientation.z
orientation.w
```

---

# 3. Movement Commands

## Straight

```bash
gz topic -t /cmd_vel \
-m gz.msgs.Twist \
-p 'linear: {x: 0.2}, angular: {z: 0.0}'
```

## Curved

```bash
gz topic -t /cmd_vel \
-m gz.msgs.Twist \
-p 'linear: {x: 0.2}, angular: {z: 0.2}'
```

## Rotation

```bash
gz topic -t /cmd_vel \
-m gz.msgs.Twist \
-p 'linear: {x: 0.0}, angular: {z: 0.2}'
```

## Stop

```bash
gz topic -t /cmd_vel \
-m gz.msgs.Twist \
-p 'linear: {x: 0.0}, angular: {z: 0.0}'
```

---

# 4. Bridge Debugging

During setup, `/odom` and ROS2 JointState became silent.

I checked the system from the source instead of immediately changing the odometry code.

The debugging path was:

```text
Gazebo robot
    ↓
JointStatePublisher
    ↓
Gazebo joint_state
    ↓
ros_gz_bridge
    ↓
ROS2 JointState
    ↓
odometry_node.py
    ↓
/odom
```

The Gazebo JointState topic existed:

```text
/world/restaurant_world/model/restaurant_robot/joint_state
```

Gazebo itself was publishing valid wheel measurements.

Example:

```text
left_wheel_joint
position ≈ 21.222 rad
velocity ≈ 2.0 rad/s

right_wheel_joint
position ≈ 21.222 rad
velocity ≈ 2.0 rad/s
```

However, ROS2 showed:

```text
Publisher count: 0
Subscriber count: 1
```

The odometry subscriber was waiting, but no ROS2 publisher was providing the data.

Inspecting:

```bash
ros2 node info /ros_gz_bridge
```

revealed a typo:

```text
restautrant_robot
```

instead of:

```text
restaurant_robot
```

After fixing the bridge topic spelling, ROS2 received JointState messages again.

### Lesson

When a downstream node becomes silent, debug the pipeline from the source instead of immediately modifying the node.

---

# 5. Scientific Notation

ROS2 and Gazebo frequently print very small values using scientific notation.

Example:

```text
7.2e-4
```

means:

```text
0.00072
```

Rule:

```text
e-N
→ move decimal N places left

e+N
→ move decimal N places right
```

Example:

```text
4.5e-3 = 0.0045
7.2e-4 = 0.00072
```

Values such as:

```text
1e-17
1e-13
1e-27
```

are extremely close to zero for the scale of these robot experiments.

For manual calculations I now round positions to approximately four decimal places.

Example:

```text
6.324953929379538
→ 6.3250 m
```

This makes experimental calculations easier while preserving enough precision.

---

# 6. Experimental Reset Rule

An important experimental-control lesson was learned.

Respawning the Gazebo robot does not automatically reset:

```python
self.x
self.y
self.theta
self.previous_left_angle
self.previous_right_angle
```

inside the already-running odometry node.

Therefore, after respawning/resetting the robot, I should restart the custom odometry node before beginning a clean new trial.

Otherwise the estimator may contain previous state and create an invalid comparison.

For each clean trial:

```text
Respawn/reset robot
        ↓
let robot settle
        ↓
restart odometry node
        ↓
verify odom ≈ (0,0,0)
        ↓
record Gazebo starting pose
        ↓
run experiment
```

---

# 7. Position Error

For a controlled trial:

```text
Δx_odom = odom_final_x - odom_start_x
Δy_odom = odom_final_y - odom_start_y

Δx_gz = gz_final_x - gz_start_x
Δy_gz = gz_final_y - gz_start_y
```

Then:

```text
error_x = Δx_odom - Δx_gz
error_y = Δy_odom - Δy_gz
```

The total 2D endpoint position error is:

```text
position_error =
sqrt(error_x² + error_y²)
```

This gives the distance between the estimated endpoint and the Gazebo endpoint.

---

# 8. Quaternion to Yaw

ROS2 and Gazebo represent orientation using quaternions:

```text
x
y
z
w
```

For planar mobile robot motion, the important angle is yaw.

General quaternion-to-yaw equation:

```text
yaw = atan2(
    2(wz + xy),
    1 - 2(y² + z²)
)
```

When quaternion x and y are approximately zero:

```text
yaw ≈ 2 * atan2(z, w)
```

Radians can be converted to degrees:

```text
degrees = radians × 180 / pi
```

Important lesson:

```text
DO NOT subtract quaternion z or w directly
to calculate heading error.
```

Instead:

```text
quaternion
    ↓
convert to yaw
    ↓
compare yaw angles
```

Also:

```text
q
```

and:

```text
-q
```

represent the same physical rotation.

Therefore opposite quaternion signs do not automatically mean opposite robot orientations.

---

# 9. Straight-Motion Baseline

Two clean repeated straight trials were completed.

Both started approximately at:

```text
odom:
x = 0
y = 0

Gazebo:
x = 0
y = 0
```

During straight motion:

```text
x changed
y stayed approximately zero
yaw stayed approximately zero
```

This confirmed the trials were clean straight runs.

---

## Straight Trial 1

Odometry:

```text
x = 2.366600 m
```

Gazebo:

```text
x = 2.366113 m
```

Signed error:

```text
2.366600 - 2.366113
≈ +0.000487 m
```

Therefore:

```text
error ≈ +0.49 mm
```

Relative error was approximately:

```text
0.021%
```

---

## Straight Trial 2

Odometry:

```text
x = 2.824600 m
```

Gazebo:

```text
x = 2.824113 m
```

Signed error:

```text
2.824600 - 2.824113
≈ +0.000487 m
```

Therefore:

```text
error ≈ +0.49 mm
```

Relative error was approximately:

```text
0.017%
```

---

# 10. Straight-Motion Result

The most interesting result was that both straight trials produced almost exactly the same absolute error:

```text
Trial 1 ≈ +0.49 mm
Trial 2 ≈ +0.49 mm
```

Therefore, under clean flat straight motion:

> The custom odometry closely matches Gazebo ground truth.

The remaining bias is extremely small and repeatable.

This suggests that basic forward-distance estimation is not currently the main weakness of the odometry implementation.

---

# 11. Why Curved Motion Is More Demanding

Straight movement mostly tests forward displacement.

During a curve:

```text
left wheel distance != right wheel distance
```

Therefore the odometry must correctly calculate:

```text
Δs
Δtheta
theta
Δx
Δy
```

The chain becomes:

```text
different wheel distances
        ↓
estimated rotation
        ↓
changing heading
        ↓
movement projected into x and y
```

A small heading error can therefore create errors in both x and y.

---

# 12. Wheel Separation Sensitivity

Differential-drive orientation change is:

```text
Δtheta =
(ΔsR - ΔsL) / wheel_separation
```

During straight motion:

```text
ΔsR - ΔsL ≈ 0
```

so wheel separation has little influence.

During turning:

```text
ΔsR - ΔsL != 0
```

so wheel separation becomes important.

If the wheel separation used by the estimator is slightly wrong:

```text
wrong wheel separation
        ↓
wrong Δtheta
        ↓
wrong theta
        ↓
wrong x/y projection
        ↓
pose error
```

This is one of the next variables to investigate experimentally.

---

# 13. Controlled Curved Trials

Several curved trials were performed on flat ground.

The clean repeated results showed much more error than the straight-motion tests, although the errors were still relatively small.

---

## Curved Trial 1

Odometry:

```text
x = -0.87382 m
y =  1.48625 m
```

Gazebo:

```text
x = -0.86760 m
y =  1.47634 m
```

Errors:

```text
x error ≈ -0.00623 m
y error ≈ +0.00991 m
```

2D endpoint error:

```text
≈ 0.01170 m
≈ 1.17 cm
```

Yaw comparison:

```text
odom yaw ≈ -119.09°
Gazebo yaw ≈ -119.21°
```

Heading error:

```text
≈ +0.11°
```

---

## Curved Trial 2

Odometry:

```text
x = -0.86150 m
y =  1.50777 m
```

Gazebo:

```text
x = -0.85490 m
y =  1.49838 m
```

Errors:

```text
x error ≈ -0.00660 m
y error ≈ +0.00939 m
```

2D endpoint error:

```text
≈ 0.01147 m
≈ 1.15 cm
```

Yaw:

```text
odom yaw ≈ -120.52°
Gazebo yaw ≈ -120.63°
```

Heading error:

```text
≈ +0.11°
```

---

## Curved Trial 3

Odometry:

```text
x = -0.98678 m
y =  1.16207 m
```

Gazebo:

```text
x = -0.98025 m
y =  1.15728 m
```

Errors:

```text
x error ≈ -0.00653 m
y error ≈ +0.00479 m
```

2D endpoint error:

```text
≈ 0.00810 m
≈ 0.81 cm
```

Yaw:

```text
odom yaw ≈ -99.33°
Gazebo yaw ≈ -99.13°
```

Heading error:

```text
≈ -0.20°
```

This trial did not finish at the same turning angle as Trials 1 and 2, so it should not be treated as a perfectly identical-duration repetition.

---

## Curved Trial 4

Odometry:

```text
x = -0.99415 m
y =  0.89200 m
```

Gazebo:

```text
x = -0.98510 m
y =  0.88700 m
```

Errors:

```text
x error ≈ -0.00905 m
y error ≈ +0.00500 m
```

2D endpoint error:

```text
≈ 0.01033 m
≈ 1.03 cm
```

Yaw:

```text
odom yaw ≈ -83.80°
Gazebo yaw ≈ -83.37°
```

Heading error:

```text
≈ -0.43°
```

---

# 14. Curved-Trial Comparison

Approximate results:

| Trial | X Error | Y Error | 2D Endpoint Error | Heading Error |
|---|---:|---:|---:|---:|
| 1 | -0.62 cm | +0.99 cm | 1.17 cm | +0.11° |
| 2 | -0.66 cm | +0.94 cm | 1.15 cm | +0.11° |
| 3 | -0.65 cm | +0.48 cm | 0.81 cm | -0.20° |
| 4 | -0.90 cm | +0.50 cm | 1.03 cm | -0.43° |

The average endpoint error across these four trials is approximately:

```text
1.04 cm
```

The important pattern is that the position error repeatedly remains around the centimetre scale.

Trials 1 and 2 are especially important because they produced almost identical results:

```text
Trial 1 ≈ 1.17 cm
Trial 2 ≈ 1.15 cm
```

and almost identical heading errors:

```text
≈ +0.11°
```

This suggests that at least part of the curved-motion error is repeatable rather than completely random.

---

# 15. Earlier Curved Test – Direction Error

In another curved run:

```text
Odometry:
x ≈ 0.9173
y ≈ 2.6868

Gazebo:
x ≈ 0.9513
y ≈ 2.6651
```

The endpoint position error was approximately:

```text
4.04 cm
```

The displacement magnitudes were very similar:

```text
Odometry displacement ≈ 2.8391 m
Gazebo displacement ≈ 2.8298 m
```

Difference:

```text
≈ 0.93 cm
```

However, the travel direction differed slightly.

The geometric analysis suggested approximately:

```text
distance-magnitude component ≈ 0.93 cm

direction-related component ≈ 3.92 cm

total endpoint error ≈ 4.04 cm
```

This showed an important robotics lesson:

> A small angular or directional error can create a much larger endpoint position error after travelling several metres.

This does not prove that the error came specifically from wheel separation or slip.

It only shows that directional disagreement contributed strongly to the endpoint difference.

---

# 16. Complex-Motion Stress Test

One experiment used changing commands instead of a single controlled command.

The robot was given different:

```text
linear velocities
angular velocities
```

during the run.

This produced a significantly larger final disagreement.

Corrected Gazebo final pose included:

```text
x ≈ 0.1883 m
y ≈ 5.1714 m
```

The custom odometry was approximately:

```text
x ≈ 0.3139 m
y ≈ 5.0261 m
```

Errors were approximately:

```text
x error ≈ +0.1256 m
y error ≈ -0.1453 m
```

2D endpoint error:

```text
≈ 0.192 m
≈ 19.2 cm
```

This trial is not directly comparable with the controlled repeated trials because the commands changed during the motion.

I classify it as:

```text
Complex Motion Stress Test
```

rather than a clean baseline trial.

---

# 17. Importance of Experimental Control

Several early experiments produced confusing results.

Examples included:

- robot respawned without resetting odometry
- different amounts of motion between trials
- accidentally copying Gazebo z as y
- orientation values copied from the wrong field
- changing commands during a trial intended to be controlled

Instead of deleting these mistakes, they taught an important lesson:

> Experimental procedure matters as much as the formula.

A clean comparison requires:

```text
same starting condition
same estimator reset
same motion command
same measurement fields
same coordinate interpretation
same comparison method
```

This is part of learning experimental robotics.

---

# 18. Front Caster / Balance Wheel

My robot has a third front support wheel / caster for balance.

This wheel is not directly used in the differential-drive odometry equations.

The odometry is calculated from:

```text
left drive wheel
right drive wheel
```

However, the caster can still influence physical robot motion through Gazebo physics.

Possible effects include:

- friction
- drag during turning
- imperfect alignment
- weight distribution
- ground contact
- resistance to rotation

Therefore:

```text
caster not part of odometry math
```

does not mean:

```text
caster cannot affect real/simulated robot motion
```

Caster influence should be tested later as a separate experiment.

---

# 19. Current Experimental Conclusion

The current evidence suggests:

## Clean Straight Motion

```text
very accurate
error ≈ 0.49 mm
repeatable
```

## Controlled Curved Motion

```text
endpoint error ≈ 0.8–1.2 cm
heading error generally small
repeatable pattern visible
```

## More Complex Changing Motion

```text
error can become much larger
```

Therefore:

> The current custom odometry performs extremely well during clean straight motion, while turning introduces a small but repeatable pose disagreement.

The current evidence does **not yet identify the exact cause**.

Possible causes still to investigate include:

- wheel separation parameter
- wheel-ground contact
- caster interaction
- turning slip
- model geometry
- integration approximation
- simulation dynamics

---

# 20. Why I Am Not Modifying odometry_node.py Yet

At this stage, changing the odometry code immediately would be premature.

The correct research process is:

```text
implementation
      ↓
baseline measurement
      ↓
repeatability testing
      ↓
identify likely cause
      ↓
change ONE variable
      ↓
repeat same experiment
      ↓
compare results
      ↓
decide whether change improved accuracy
```

If I change multiple things before establishing the baseline, I cannot know which change caused an improvement or regression.

---

# 21. Next Experiment – Wheel Separation Sensitivity

The next planned experiment is to investigate whether wheel separation contributes to the turning bias.

Current formula:

```text
Δtheta =
(ΔsR - ΔsL) / wheel_separation
```

The plan is to keep the physical simulation unchanged while changing the wheel-separation value used by the custom odometry estimator.

Example experiment:

```text
Baseline:
b = 0.60 m

Test A:
slightly smaller b

Test B:
slightly larger b
```

Then run the same curved motion and compare:

```text
position error
heading error
```

Only one variable should change at a time.

This is a parameter-sensitivity experiment.

---

# 22. Later Experiments

After wheel-separation sensitivity:

```text
1. Caster influence

2. Longer straight travel

3. Longer curved travel

4. Wheel slip

5. Collision / wheel spinning while stuck

6. Wrong wheel radius

7. Slope / uphill motion

8. Downhill motion
```

Slope testing is especially relevant to restaurant/service robots because real environments may contain:

- ramps
- uneven floors
- wet floors
- changes in wheel contact

These conditions can make encoder-only odometry less reliable.

---

# What I Learned

The main lesson from this checkpoint is that implementing odometry is only the beginning.

A robotics system should also be:

```text
measured
tested
repeated
compared
diagnosed
```

I learned that:

1. `/odom` and TF agreement proves consistency, not accuracy.

2. Gazebo ground truth provides an independent reference.

3. Clean resets are necessary before controlled experiments.

4. Straight motion can hide turning-related errors.

5. Curved motion tests more of the differential-drive model.

6. A small heading error can create centimetres of endpoint error.

7. Quaternion components should not be compared directly as angles.

8. Scientific notation is common in robotics output.

9. Repeated trials help distinguish repeatable bias from random variation.

10. Experimental mistakes can reveal weaknesses in the testing procedure.

11. I should not change the implementation until I have enough baseline evidence.

12. Changing one variable at a time allows me to identify causality.

---

# Learning Evidence

During this checkpoint I:

- restored and debugged the Gazebo → ROS2 JointState bridge
- identified a misspelled bridge topic
- verified Gazebo JointState values
- restored `/odom`
- learned scientific notation used by ROS2/Gazebo
- learned to round experimental values appropriately
- learned quaternion-to-yaw conversion
- learned that `q` and `-q` represent the same rotation
- designed controlled straight and curved experiments
- measured odometry against Gazebo ground truth
- repeated straight-motion trials
- repeated curved-motion trials
- calculated x error
- calculated y error
- calculated 2D endpoint error
- calculated heading error
- identified repeatable curved-motion disagreement
- compared simple motion with complex-motion stress tests
- identified possible turning-related variables
- developed a more controlled experimental procedure

---

# Research Transition

The project is now moving from:

```text
"I wrote an odometry node."
```

toward:

```text
"I implemented an odometry estimator,
validated it against independent ground truth,
measured its error,
tested repeatability,
and am designing experiments to identify
the source of the remaining error."
```

This is the direction I want for the rest of the project.

---

# Resume Point

Next session:

```text
WHEEL-SEPARATION SENSITIVITY EXPERIMENT

1. Keep Gazebo robot geometry unchanged
2. Record baseline wheel separation
3. Run controlled curved baseline
4. Modify estimator wheel separation slightly
5. Repeat identical curved command
6. Record endpoint error
7. Record heading error
8. Compare against baseline
9. Decide how wheel separation affects the result
```

Do not modify multiple parameters at the same time.

After the wheel-separation experiment:

```text
caster interaction
→ slip
→ slopes
→ longer trajectories
```
