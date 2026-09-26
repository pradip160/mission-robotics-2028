# Day 61 – Curved Odometry Error Diagnosis

Date: 26 September 2026

## Goal

The goal of this study block was to investigate a question left from the previous odometry-validation experiments:

> Why does my custom differential-drive odometry remain extremely accurate during straight motion but develop a small, repeatable error during curved motion?

Instead of randomly changing parameters, I tested possible causes one at a time.

The investigation included:

- wheel-separation sensitivity
- caster friction
- drive-wheel friction
- intentional low-grip conditions
- pure rotation
- speed-dependent curved motion
- odometry update frequency
- Gazebo ground-truth update frequency
- determining which Gazebo topics are independent ground truth
- narrowing the next hypothesis toward small physical lateral/contact effects

---

# 1. Starting Evidence

From the previous experiments:

## Straight motion

Two clean straight trials produced approximately:

```text
error ≈ +0.49 mm
```

The robot remained approximately:

```text
y ≈ 0
yaw ≈ 0
```

This showed that forward-distance estimation was already extremely accurate.

---

## Curved motion

Controlled curved trials produced approximately:

```text
endpoint error ≈ 0.8–1.2 cm
```

The error was repeatable rather than strongly random.

Therefore the main investigation became:

```text
Why does turning while translating create more error
than straight motion?
```

---

# 2. Wheel-Separation Sensitivity

The differential-drive turning equation is:

```text
Δtheta = (ΔsR - ΔsL) / wheel_separation
```

The physical Gazebo wheel separation remained:

```text
0.60 m
```

Only the value used inside my custom odometry estimator was changed.

This was important because it separated:

```text
physical robot geometry
```

from:

```text
what the estimator believes the geometry is
```

---

## Estimator = 0.58 m

Three repeated curved trials produced approximately:

```text
endpoint error ≈ 19–20 cm
heading disagreement ≈ 10°
```

The result was highly repeatable.

---

## Estimator = 0.60 m

With the correct value:

```text
endpoint error ≈ 1 cm
```

The disagreement became dramatically smaller.

---

## Estimator = 0.62 m

Two trials produced approximately:

```text
endpoint error ≈ 21 cm
heading disagreement ≈ 10°
```

The error direction also changed compared with the 0.58 m condition.

---

# 3. Wheel-Separation Conclusion

The experiment strongly supported:

```text
wheel_separation = 0.60 m
```

for this robot.

A small error in wheel separation can produce a very large turning error because:

```text
smaller assumed separation
→ larger calculated Δtheta

larger assumed separation
→ smaller calculated Δtheta
```

Straight motion is much less sensitive because:

```text
ΔsR - ΔsL ≈ 0
```

therefore:

```text
Δtheta ≈ 0
```

even if the wheel-separation value is slightly wrong.

### Conclusion

Wheel separation is extremely important for curved motion, but the remaining ~1 cm baseline error is not explained by an incorrect wheel-separation value because 0.60 m already gives the best result.

---

# 4. Inspecting the Front Caster

The SDF showed that the front support is represented by a sphere attached rigidly to `base_link`.

Example:

```xml
<collision name='base_link_fixed_joint_lump__front_caster_collision_1'>
  <pose>0.30 0 0 0 0 0</pose>

  <geometry>
    <sphere>
      <radius>0.05</radius>
    </sphere>
  </geometry>
</collision>
```

This means it is not a freely swivelling caster in the physical model.

It acts more like:

```text
base_link
   |
   └── fixed support sphere
```

Even though this sphere is not part of the odometry equations, its contact with the floor could still influence actual Gazebo motion.

---

# 5. Caster-Friction Experiment

I tested whether caster-ground friction was responsible for the curved-motion error.

The low-friction condition used:

```xml
<surface>
  <friction>
    <ode>
      <mu>0.01</mu>
      <mu2>0.01</mu2>
    </ode>
  </friction>
</surface>
```

Three controlled low-friction trials around 20.4–20.5 seconds produced approximately:

```text
2D endpoint error:
1.24 cm
1.27 cm
1.31 cm

yaw error:
≈ -0.48°
```

Then I restored the normal caster condition.

Two normal-caster trials produced approximately:

```text
2D endpoint error:
1.10 cm
1.11 cm

yaw error:
≈ +0.11°
```

---

# 6. Caster Conclusion

Reducing caster friction did not remove the odometry error.

The error stayed at approximately the same centimetre scale.

Therefore:

> The caster affects the physical trajectory slightly, but it does not appear to be the main source of the curved-motion odometry error.

This is a secondary influence rather than the dominant cause.

---

# 7. Drive-Wheel Friction Experiment

The left and right wheels originally had no explicit friction settings.

Their collision definitions relied on Gazebo's default contact behaviour.

I deliberately reduced drive-wheel friction to test whether wheel-ground grip strongly affects odometry accuracy.

For both drive wheels I added:

```xml
<surface>
  <friction>
    <ode>
      <mu>0.1</mu>
      <mu2>0.1</mu2>
    </ode>
  </friction>
</surface>
```

Everything else remained unchanged.

---

# 8. Low-Friction Drive-Wheel Results

## Trial 1

Approximately:

```text
x error ≈ -5.06 cm
y error ≈ -2.01 cm

2D endpoint error ≈ 5.45 cm

yaw error ≈ +1.47°
```

## Trial 2

Approximately:

```text
x error ≈ -4.90 cm
y error ≈ -2.00 cm

2D endpoint error ≈ 5.29 cm

yaw error ≈ +1.47°
```

The two trials were highly repeatable.

---

# 9. Drive-Wheel Friction Conclusion

Normal curved baseline:

```text
endpoint error ≈ 1.1 cm
yaw error ≈ 0.11°
```

Low wheel friction:

```text
endpoint error ≈ 5.3–5.5 cm
yaw error ≈ 1.47°
```

Therefore reducing wheel grip increased endpoint error by roughly five times.

This gives strong experimental evidence that:

> Encoder odometry is highly sensitive to wheel-ground contact and slip.

However, this does not prove that the entire original ~1 cm baseline error is caused by slip.

The low-friction experiment only proves that reduced grip can create much larger odometry error.

---

# 10. Pure-Rotation Experiment

The next question was:

> Is the remaining problem mainly caused by incorrect turning-angle estimation?

I performed three pure-rotation trials.

The command used:

```text
linear.x = 0
angular.z = 0.2
```

The runs were approximately 20 seconds.

---

## Pure Rotation Results

### Trial 1

Gazebo translated approximately:

```text
5.61 mm
```

Yaw disagreement:

```text
≈ 0.015°
```

### Trial 2

Gazebo translated approximately:

```text
5.60 mm
```

Yaw disagreement:

```text
≈ 0.015°
```

### Trial 3

Gazebo translated approximately:

```text
5.62 mm
```

Yaw disagreement:

```text
≈ 0.015°
```

---

# 11. Pure-Rotation Conclusion

The yaw estimation during pure rotation was extremely accurate.

Therefore the basic turning equation:

```text
Δtheta = (ΔsR - ΔsL) / b
```

does not appear to be the main problem.

However, Gazebo physically translated about:

```text
5.6 mm
```

while the ideal odometry model predicted approximately:

```text
x = 0
y = 0
```

during pure rotation.

This was an important observation.

It shows that the simulated robot does not behave as a perfectly ideal differential-drive model.

Small contact or physical effects can create motion that wheel-only odometry does not represent.

---

# 12. Speed-Sensitivity Experiment

Another important observation was that curved-motion error changed with speed.

To keep the same theoretical turning radius:

```text
R = v / omega
```

I kept:

```text
v = omega
```

---

## Faster curved motion

For:

```text
linear.x  = 0.20 m/s
angular.z = 0.20 rad/s
```

three approximately 10-second trials produced:

```text
1.56 cm
1.61 cm
1.54 cm
```

Average endpoint error:

```text
≈ 1.57 cm
```

The error direction was also highly repeatable.

---

## Slower curved motion

For:

```text
linear.x  = 0.10 m/s
angular.z = 0.10 rad/s
```

three approximately 20-second trials produced:

```text
0.47 cm
0.45 cm
0.47 cm
```

Average endpoint error:

```text
≈ 0.46 cm
```

Therefore:

```text
fast curve ≈ 1.57 cm error
slow curve ≈ 0.46 cm error
```

The slower condition produced roughly 70% less endpoint error.

---

# 13. Important Speed Result

This strongly suggested:

> The curved-motion disagreement is speed dependent.

However, speed dependence alone does not identify the exact cause.

Possible causes include:

- wheel-ground contact dynamics
- tiny lateral slip
- weight transfer
- pitching during acceleration
- transient wheel loading
- non-ideal differential-drive physics

---

# 14. Startup Pitching Observation

During higher-speed tests I visually noticed that the robot rocked or pitched up/down when commanded to start quickly.

Example:

```text
0.00 → 0.35
```

caused noticeable chassis movement.

When speed was increased gradually:

```text
0.00
→ 0.10
→ 0.15
→ 0.25
→ 0.35
```

the robot appeared more stable.

This suggested that sudden acceleration changes:

```text
wheel force
weight distribution
wheel contact
robot pitch
```

and may therefore contribute to non-ideal motion.

A long gradual-ramp experiment produced approximately:

```text
endpoint error ≈ 3.49 cm
yaw error ≈ -1.44°
```

but this result could not be directly compared with shorter abrupt-start experiments because the total trajectory length and duration were different.

Therefore this remains a qualitative observation rather than a fully isolated causal result.

---

# 15. Why More Endpoint Experiments Were Not Enough

At this stage I realized that endpoint comparisons tell me:

```text
the final pose is different
```

but do not tell me:

```text
where during the trajectory the error appeared
```

or:

```text
what physical motion created it
```

Therefore continuing to change parameters randomly would not be good research methodology.

The next investigation should compare motion continuously during the curve.

---

# 16. JointState Frequency

I measured:

```bash
ros2 topic hz /world/restaurant_world/model/restaurant_robot/joint_state
```

Result:

```text
average rate ≈ 1000 Hz
```

Therefore:

```text
Δt ≈ 0.001 s
```

At:

```text
v = 0.20 m/s
```

the robot travels only approximately:

```text
0.0002 m
= 0.2 mm
```

per JointState update.

At:

```text
omega = 0.20 rad/s
```

the orientation increment per update is approximately:

```text
0.0002 rad
```

This is extremely small.

---

# 17. Numerical Integration Hypothesis

My odometry uses midpoint integration:

```text
theta_mid = theta + Δtheta / 2

Δx = Δs * cos(theta_mid)

Δy = Δs * sin(theta_mid)
```

Initially I considered whether faster motion caused larger numerical integration error.

However, because JointState updates arrive at approximately:

```text
1000 Hz
```

the integration steps are already extremely small.

Therefore coarse integration error is now a much weaker explanation for centimetre-scale disagreement.

This shifts attention back toward physical simulation/contact effects.

---

# 18. Inspecting Gazebo Odometry

Gazebo publishes:

```text
/model/restaurant_robot/odometry
```

I inspected it with:

```bash
gz topic -i -t /model/restaurant_robot/odometry
```

and:

```bash
gz topic -e -t /model/restaurant_robot/odometry
```

The pose was almost numerically identical to my custom odometry.

Example Gazebo odometry:

```text
x = -0.8882503033
y =  1.4593597704
```

Custom odometry from the same run:

```text
x = -0.8882503103
y =  1.4593597730
```

These are essentially the same.

Therefore:

> `/model/restaurant_robot/odometry` is not an independent ground-truth measurement for this experiment.

It appears to be based on the same ideal differential-drive/wheel-motion model.

---

# 19. Independent Ground Truth

The independent reference remains:

```text
/world/restaurant_world/dynamic_pose/info
```

because this reports the robot pose produced by Gazebo physics.

---

# 20. Ground-Truth Frequency

I measured:

```bash
gz topic -f -t /world/restaurant_world/dynamic_pose/info
```

Typical result:

```text
average rate ≈ 59 Hz
```

Therefore:

```text
Δt ≈ 0.017 s
```

The messages also contain simulation timestamps.

Example:

```text
sec: 1412
nsec: 211000000
```

followed by:

```text
sec: 1412
nsec: 228000000
```

Difference:

```text
17 ms
```

which matches the approximately 59 Hz publication rate.

---

# 21. Current Measurement Architecture

I now have:

```text
Wheel JointState:
≈ 1000 Hz

Gazebo ground truth:
≈ 59 Hz
```

This is enough to compare:

```text
wheel-predicted motion
vs
actual simulated physical motion
```

The two streams do not need to have identical frequencies.

---

# 22. New Diagnostic Direction

Instead of comparing only final endpoints, the next investigation will measure actual robot motion during the curve.

From wheel motion:

```text
v_wheel =
(ΔsR + ΔsL) / (2 * Δt)

omega_wheel =
(ΔsR - ΔsL) / (wheel_separation * Δt)
```

From consecutive Gazebo ground-truth poses:

```text
Δx = x2 - x1
Δy = y2 - y1
Δtheta = theta2 - theta1
Δt = t2 - t1
```

This will allow comparison of:

```text
wheel-predicted forward motion
wheel-predicted turning

vs

actual Gazebo forward motion
actual Gazebo turning
```

---

# 23. Possible Lateral Slip

The next concept to investigate is small sideways motion.

An ideal differential-drive robot assumes:

```text
forward movement
+ rotation
```

but approximately:

```text
no sideways velocity in the robot's own frame
```

The robot can still change both world `x` and `y` because its forward direction continuously rotates.

However, Gazebo physics may allow:

```text
forward movement
+ rotation
+ tiny sideways sliding
```

Wheel encoders cannot directly observe that sideways motion.

If this occurs, it could explain why:

```text
straight motion → extremely accurate

pure rotation yaw → extremely accurate

curved motion → small repeatable error

higher-speed curved motion → larger error
```

This is now the next hypothesis to investigate.

---

# Current Conclusions

The experiments have narrowed the problem substantially.

## Strongly supported

```text
Wheel separation = 0.60 m
```

Changing it by only ±0.02 m creates very large turning errors.

---

## Caster

```text
secondary influence
```

Changing caster friction modifies the trajectory slightly but does not remove the curved-motion error.

---

## Drive-wheel grip

```text
major influence
```

Artificially reducing wheel friction increased endpoint error from approximately:

```text
1.1 cm
```

to:

```text
5.3–5.5 cm
```

Therefore wheel-ground contact strongly affects odometry accuracy.

---

## Pure rotation

```text
yaw estimation ≈ extremely accurate
```

but Gazebo still shows approximately:

```text
5.6 mm
```

of physical translation during nominal pure rotation.

---

## Speed

```text
slow curve ≈ 0.46 cm error
fast curve ≈ 1.57 cm error
```

Therefore curved-motion error is speed dependent.

---

## Numerical integration

Because wheel updates occur at approximately:

```text
1000 Hz
```

coarse numerical integration is unlikely to be the main explanation.

---

## Remaining hypothesis

The remaining error is likely related to non-ideal physical motion during simultaneous translation and rotation.

Possible effects include:

```text
small lateral slip
contact deformation / simulation contact effects
weight transfer
pitching
speed-dependent wheel-ground interaction
```

The exact cause has not yet been proven.

---

# What I Learned

Today I learned that debugging robotics accuracy is not about changing values until the result looks correct.

A better process is:

```text
observe
↓
form hypothesis
↓
change one variable
↓
repeat experiment
↓
compare against ground truth
↓
reject or support hypothesis
↓
narrow the next question
```

I also learned:

1. Wheel separation strongly affects turning accuracy.

2. Straight motion cannot fully validate differential-drive geometry.

3. A physical component can influence motion even if it is not part of the odometry equation.

4. Caster friction was only a secondary effect in this robot.

5. Wheel-ground friction strongly affects encoder odometry.

6. Wheel slip does not always need to look visually dramatic.

7. Pure rotation can have accurate yaw while the physical robot still translates slightly.

8. Speed-dependent error suggests physical dynamics are important.

9. A high estimator update rate makes coarse integration error less likely.

10. Gazebo's own DiffDrive odometry is not independent ground truth.

11. `/world/restaurant_world/dynamic_pose/info` remains the correct independent physics reference.

12. Endpoint error tells me that something went wrong, but continuous measurements are needed to determine where it went wrong.

---

# Learning Evidence

During this checkpoint I:

- tested wheel-separation sensitivity
- confirmed 0.60 m as the best estimator value
- performed repeated 0.58 m and 0.62 m incorrect-parameter trials
- investigated the front caster model
- performed controlled caster-friction experiments
- classified caster friction as a secondary influence
- changed drive-wheel friction experimentally
- measured approximately five-times larger error under low wheel grip
- performed three pure-rotation trials
- measured extremely small pure-rotation yaw disagreement
- discovered small repeatable physical translation during nominal pure rotation
- compared slow and fast curved trajectories
- discovered strong speed dependence
- observed startup pitching at higher acceleration
- investigated gradual acceleration
- measured the JointState publication rate
- confirmed approximately 1000 Hz wheel-state updates
- rejected coarse numerical integration as the leading hypothesis
- inspected Gazebo's `/model/restaurant_robot/odometry`
- determined that it is not independent ground truth
- measured `/world/restaurant_world/dynamic_pose/info` at approximately 59 Hz
- verified simulator timestamps
- identified continuous wheel-vs-physics motion comparison as the next research step

---

# Research Progress

The project has moved from:

```text
"My curved odometry has about 1 cm error."
```

toward:

```text
"I have experimentally tested multiple possible causes,
eliminated incorrect wheel separation and caster friction
as dominant explanations,
demonstrated strong sensitivity to drive-wheel grip,
identified speed-dependent error,
verified that pure rotational yaw is highly accurate,
and narrowed the next investigation toward
non-ideal physical motion during simultaneous
translation and rotation."
```

This is a much stronger research position than simply tuning parameters.

---

# Resume Point

Next session:

## Continuous Motion Diagnosis

Do not perform more random endpoint tests.

The next goal is to compare wheel-predicted motion against Gazebo physics during the trajectory.

Use:

```text
Wheel JointState
≈ 1000 Hz

Gazebo dynamic_pose
≈ 59 Hz
```

Investigate:

```text
wheel-predicted forward velocity
wheel-predicted angular velocity

vs

actual Gazebo forward motion
actual Gazebo angular motion
```

Then learn how to transform world-frame movement into the robot's own frame.

Main question:

> During a curved trajectory, does Gazebo show a small sideways motion that the ideal differential-drive odometry cannot observe?

If sideways motion exists consistently and increases with speed, that would provide direct evidence of non-ideal wheel-ground/contact behaviour.

Do not change the robot geometry or odometry parameters before measuring this.
