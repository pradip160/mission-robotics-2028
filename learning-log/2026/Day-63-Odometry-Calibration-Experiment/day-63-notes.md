# Day 63 — Odometry Physical Model Investigation and Calibration

## Starting Point

This work continued from Day 62, where I created a Gazebo ground-truth motion diagnostic.

At the start of this investigation I already had:

- Custom ROS2 differential-drive odometry
- `/odom`
- `odom -> base_link` TF
- Gazebo robot simulation
- Wheel encoder / JointState input
- Gazebo ground-truth pose
- A Python ground-truth diagnostic calculating:
  - `v_forward`
  - `v_sideways`
  - `omega`

The purpose of this investigation was to understand why mathematically correct odometry did not always match the robot's real physical motion inside Gazebo.

---

# 1. Ground Truth Diagnostic Improvement

The diagnostic reads:

`/world/restaurant_world/dynamic_pose/info`

and converts Gazebo quaternion orientation into yaw.

It then calculates motion between consecutive samples.

Important quantities:

`delta_x`

`delta_y`

`delta_theta`

`delta_t`

The world-frame displacement is projected into the robot frame.

Forward displacement:

`forward = delta_x*cos(theta_mid) + delta_y*sin(theta_mid)`

Sideways displacement:

`sideways = -delta_x*sin(theta_mid) + delta_y*cos(theta_mid)`

Then:

`v_forward = forward / delta_t`

`v_sideways = sideways / delta_t`

`omega = delta_theta / delta_t`

This allowed direct comparison between:

- Wheel-based ROS2 odometry
- Actual Gazebo physics motion

---

# 2. Timestamp Bug

The Gazebo protobuf JSON sometimes omitted `nsec` when nanoseconds were exactly zero.

Originally:

`stamp["nsec"]`

could cause:

`KeyError: nsec`

The fix was:

`stamp.get("nsec", 0)`

The final timestamp calculation became:

`time = sec + nsec * 1e-9`

This was important because using only integer seconds produced poor velocity measurements.

After fixing this, the ground-truth diagnostic produced high-frequency and reliable velocity measurements.

---

# 3. Initial Curved-Motion Problem

The odometry equations used:

`wheel radius = 0.10 m`

`wheel separation = 0.60 m`

Differential-drive equations:

`v = (v_R + v_L) / 2`

`omega = (v_R - v_L) / b`

During some curved-motion experiments, ROS2 odometry predicted approximately:

`v = 0.20 m/s`

`omega = 0.20 rad/s`

but Gazebo physics did not always produce exactly the same motion.

This started the calibration investigation.

---

# 4. Wheel Radius Investigation

Straight-line motion was tested first.

Straight commands produced approximately the expected forward velocity.

This showed that the wheel radius was already producing correct linear motion.

Conclusion:

`wheel radius = 0.10 m`

was not the main source of the turning error.

Therefore the wheel radius was not changed.

---

# 5. Wheel Separation Investigation

Wheel separation mainly affects angular motion.

The physical drive-wheel centers were:

`left wheel y = +0.30 m`

`right wheel y = -0.30 m`

Therefore:

`wheel center separation = 0.60 m`

Pure-rotation experiments showed that the robot could produce almost exactly the expected angular velocity with:

`wheel separation = 0.60 m`

This was strong evidence that the basic wheel-separation value was correct.

Conclusion:

Do not change wheel separation simply to compensate for other physical-model problems.

---

# 6. Fixed Front Caster Problem

The original robot used a fixed spherical front caster.

The caster was located approximately:

`x = +0.30 m`

During turning, a point located in front of the robot's rotation center needs sideways velocity.

For a point at distance `r` from the rotation center:

`v = omega * r`

For example:

`r = 0.30 m`

`omega = 0.20 rad/s`

Therefore:

`v = 0.20 * 0.30`

`v = 0.06 m/s`

The front contact therefore needed to move sideways during turning.

But the old caster was fixed.

It could not swivel and align itself with the direction of motion.

This created unrealistic lateral scrubbing/contact forces.

---

# 7. Caster Friction Experiments

The fixed caster friction was changed during experiments.

Low friction and higher friction produced different combinations of:

- Forward velocity
- Angular velocity

This showed that the front fixed contact strongly influenced curved motion.

However, changing friction did not provide a clean physical solution.

Conclusion:

The fixed spherical caster itself was the wrong physical model.

Instead of tuning friction around an unrealistic caster, I decided to build a real passive swivel caster.

---

# 8. Swivel Caster Design

The old fixed caster was removed.

A new caster system was created with three parts:

1. `caster_fork`
2. `caster_swivel_joint`
3. `caster_wheel`

The swivel joint rotates around the Z axis.

`axis = 0 0 1`

The caster wheel rolls around the Y axis.

`axis = 0 1 0`

The wheel axle was placed behind the swivel pivot to create caster trail.

Initial caster trail:

`0.04 m`

The caster wheel radius:

`0.05 m`

This created a physically meaningful passive caster that can swivel during robot motion.

---

# 9. SDF Validation

After editing the caster model, the SDF was validated using:

`gz sdf -k restaurant_robot.sdf`

The model eventually returned:

`Valid.`

This confirmed the new SDF structure was syntactically valid.

---

# 10. Accidental Base Visual Removal

During the caster edits, the `base_link_visual` section was accidentally removed.

The robot then appeared in Gazebo with wheels but without the main body.

The chassis visual was restored.

The restored chassis geometry was:

`0.8 x 0.5 x 0.2 m`

After restoring the visual, the robot body appeared correctly again.

Important lesson:

Collision, visual, inertial, and joint definitions are separate parts of the robot model.

Deleting a visual does not necessarily delete the physical collision model.

---

# 11. Robot Stability Problem

After replacing the old caster, the robot tilted backward.

The reason was related to center-of-mass placement.

The main chassis COM was approximately directly above the drive-wheel axle.

The two drive wheels form a support line.

The front caster forms the third point of the robot's support polygon.

If the COM projection moves behind the drive-wheel support line, the robot can tip backward.

I learned that the COM must remain inside the support polygon.

---

# 12. Support Polygon

For this robot, the support polygon is approximately a triangle:

- Left drive wheel
- Right drive wheel
- Front caster

The robot's center of mass should remain inside this triangle.

The drive wheels should carry most of the weight, while the caster provides additional front support and stability.

---

# 13. Base COM Calibration

The base chassis COM was moved forward.

Old:

`COM x = 0.00 m`

New:

`COM x = +0.05 m`

After this change, the robot became physically stable.

The robot remained level on:

- Left drive wheel
- Right drive wheel
- Front caster

This stability correction had to be completed before trusting further calibration measurements.

Final:

`Base COM x = +0.05 m`

---

# 14. Base Inertial Model Correction

The old base inertial values still contained the mass contribution of the original fixed caster.

The base had previously become approximately:

`mass = 10.5 kg`

with an offset COM.

After removing the old caster, the base inertial model was restored to the chassis-only values.

Final base mass:

`10.0 kg`

The old caster mass was no longer incorrectly included inside `base_link`.

This prevented double-counting caster mass after adding the new caster links.

---

# 15. Controlled Calibration Method

A major lesson from this investigation was that calibration must be controlled.

The procedure became:

1. Form a hypothesis.
2. Change only one parameter.
3. Restart Gazebo.
4. Spawn the robot fresh.
5. Run the same motion command.
6. Measure `/odom`.
7. Measure Gazebo ground truth.
8. Compare results.
9. Accept or reject the hypothesis.

Changing several parameters simultaneously would make it impossible to know which change caused the result.

---

# 16. Pure Rotation as a Diagnostic Test

Pure rotation was used to isolate angular behavior.

Example command:

`linear.x = 0.00 m/s`

`angular.z = 0.20 rad/s`

Ideal differential-drive behavior should produce:

`v_forward ≈ 0`

`v_sideways ≈ 0`

`omega ≈ 0.20 rad/s`

Pure rotation became one of the most useful calibration tests.

---

# 17. Small Translation During Pure Rotation

Even when odometry predicted:

`linear.x ≈ 0`

Gazebo ground truth showed a small forward or backward velocity during pure rotation.

For example, with a larger drive-wheel collision width:

`v_forward ≈ 0.0035 m/s`

while:

`omega ≈ 0.20 rad/s`

This indicated that the physical contact geometry was influencing the effective rotation center.

---

# 18. Caster Trail Investigation

The caster trail was changed from:

`0.04 m`

to:

`0.02 m`

Both the caster wheel link pose and the caster wheel joint pose were changed consistently.

The purpose was to test whether caster trail caused the pure-rotation translation.

Results showed that changing the trail could change contact behavior and sometimes even the sign of the small translation.

However, it did not eliminate the magnitude of the drift.

Conclusion:

Caster trail was not the primary cause of the remaining pure-rotation translation.

Final caster trail:

`0.02 m`

---

# 19. Drive-Wheel Collision Geometry Hypothesis

The drive wheels are represented by cylinders.

The visible wheel width and the collision width do not have to be identical.

The visual geometry represents how the robot looks.

The collision geometry determines how Gazebo physics calculates contact.

Ideal differential-drive mathematics assumes approximately a line contact at each wheel centerline.

A wide cylinder creates a finite-width contact region.

This means Gazebo may create contact away from the exact wheel centerline.

Hypothesis:

Reducing the drive-wheel collision width should reduce contact-related odometry error.

---

# 20. Drive Collision Width — 0.035 m

With:

`drive collision width = 0.035 m`

Pure rotation at:

`omega command = 0.20 rad/s`

produced approximately:

`|v_forward| ≈ 0.0035 m/s`

`omega ≈ 0.20 rad/s`

The unexpected translation was measurable even though angular velocity was correct.

---

# 21. Drive Collision Width — 0.020 m

The collision width was reduced to:

`0.020 m`

Everything else remained unchanged.

Pure rotation produced approximately:

`|v_forward| ≈ 0.0020 m/s`

`omega ≈ 0.20 rad/s`

The unwanted translation decreased significantly.

This supported the wheel-contact hypothesis.

---

# 22. Drive Collision Width — 0.010 m

The collision width was reduced again:

`0.010 m`

Pure rotation produced approximately:

`|v_forward| ≈ 0.0010 m/s`

`omega ≈ 0.20 rad/s`

Again, the unwanted translation decreased almost proportionally with collision width.

---

# 23. Drive Collision Width — 0.005 m

The collision width was finally reduced to:

`0.005 m`

Pure rotation produced approximately:

`v_forward ≈ 0.00050 m/s`

`v_sideways ≈ almost 0`

`omega ≈ 0.20000002 rad/s`

This was the smallest meaningful pure-rotation drift tested.

The remaining translation was very small.

---

# 24. Observed Pure-Rotation Relationship

The experiments produced approximately:

| Drive Collision Width | Pure Rotation Drift |
|---|---:|
| 0.035 m | ~0.0035 m/s |
| 0.020 m | ~0.0020 m/s |
| 0.010 m | ~0.0010 m/s |
| 0.005 m | ~0.0005 m/s |

A strong experimental relationship appeared:

`|v_forward| ≈ |omega| * collision_width / 2`

For example:

`omega = 0.20`

`collision width = 0.005`

Then:

`0.20 * 0.005 / 2 = 0.0005 m/s`

which matched the ground-truth measurement closely.

This provided strong evidence that finite wheel collision geometry was responsible for much of the pure-rotation translation.

---

# 25. Curved Motion Calibration

The standard curved-motion test used:

`linear.x = 0.20 m/s`

`angular.z = 0.20 rad/s`

ROS2 odometry predicted:

`v ≈ 0.20 m/s`

`omega ≈ 0.20 rad/s`

Ground truth was compared at different collision widths.

---

# 26. Curve Test — 0.020 m Collision Width

With:

`collision width = 0.020 m`

ground truth produced approximately:

`v_forward ≈ 0.20 m/s`

`omega ≈ 0.206896 rad/s`

Angular error:

approximately `+3.45%`

Linear velocity remained essentially correct.

---

# 27. Curve Test — 0.010 m Collision Width

With:

`collision width = 0.010 m`

ground truth produced approximately:

`v_forward ≈ 0.20 m/s`

`omega ≈ 0.203389 rad/s`

Angular error:

approximately `+1.69%`

The thinner collision geometry reduced the angular mismatch.

---

# 28. Curve Test — 0.005 m Collision Width

With:

`collision width = 0.005 m`

one fresh run produced approximately:

`v_forward ≈ 0.20 m/s`

`omega ≈ 0.198348 rad/s`

Angular error:

approximately `-0.83%`

Another fresh run produced approximately:

`omega ≈ 0.201680 rad/s`

Angular error:

approximately `+0.84%`

The average behavior was extremely close to:

`0.20 rad/s`

This showed that very small contact-state differences can move the effective wheel contact slightly inward or outward.

---

# 29. Effective Track Width Observation

For the `0.005 m` wheel collision:

One run behaved approximately like:

`effective separation = 0.600 + 0.005`

Another behaved approximately like:

`effective separation = 0.600 - 0.005`

This suggested that Gazebo contact can settle toward different sides of the finite-width wheel collision surface.

Therefore the effective wheel-ground contact line is not always exactly at the mathematical wheel center.

Reducing collision width reduces the size of this uncertainty.

---

# 30. Repeatability Testing

Several fresh Gazebo runs were performed.

The robot was respawned from a fresh simulation state between tests.

This was important because:

- Caster orientation can differ
- Wheel contacts can settle differently
- Contact solver state can differ
- Small physical transients can affect the result

At the final collision width, curved-motion angular error remained approximately within:

`±0.84%`

This was considered sufficiently small for the current ideal differential-drive simulation.

---

# 31. Opposite Direction Curve Test

The robot was also tested using:

`linear.x = 0.20 m/s`

`angular.z = -0.20 rad/s`

Ground truth produced approximately:

`v_forward ≈ 0.20 m/s`

`omega ≈ -0.20 rad/s`

The sideways velocity remained very small.

Some early samples showed approximately:

`omega ≈ -0.20168 rad/s`

and later samples settled close to:

`omega ≈ -0.20000 rad/s`

This showed that the final robot configuration worked in both turning directions.

---

# 32. Sideways Motion

Throughout the final tests:

`v_sideways`

was extremely small compared with forward velocity.

Typical values were around:

`10^-5 m/s`

or smaller.

This indicated that the robot was behaving close to the non-holonomic differential-drive assumption:

The robot should primarily move:

- Forward/backward
- Rotate

and should not freely slide sideways.

---

# 33. Final Robot Configuration

The final calibrated physical model uses:

- Wheel radius: `0.10 m`
- Wheel separation: `0.60 m`
- Drive-wheel collision width: `0.005 m`
- Caster trail: `0.02 m`
- Base COM x: `+0.05 m`
- Base chassis mass: `10.0 kg`

The wheel visual geometry can remain wider than the collision geometry.

The collision geometry is intentionally thin to better approximate the line-contact assumption used by differential-drive kinematics.

---

# 34. Why the Visual Wheel Can Stay Wide

The visual geometry controls appearance.

The collision geometry controls physical contact.

A real wheel can visually have thickness while its simplified mathematical rolling model treats the ground contact as approximately a line.

Therefore:

Visual wheel:

represents realistic appearance.

Thin collision wheel:

represents the idealized differential-drive contact used by the mathematical model.

This is a simulation-modeling decision, not a claim that the physical wheel itself is only 5 mm wide.

---

# 35. Final Calibration Performance

Final pure rotation:

`command omega = 0.20 rad/s`

Ground truth:

`omega ≈ 0.20000002 rad/s`

Forward drift:

`≈ 0.00050 m/s`

Sideways velocity:

approximately zero.

Final curved motion:

`command v = 0.20 m/s`

`command omega = ±0.20 rad/s`

Ground truth:

`v_forward ≈ 0.20 m/s`

`omega ≈ ±0.20 rad/s`

Typical fresh-run angular variation:

approximately `±0.84%`

Sideways velocity remained very small.

---

# 36. Calibration Stopping Decision

I decided not to continue shrinking the collision width.

The objective of calibration is not to force simulation error to exactly zero.

The goal is to create a model that is:

- Physically stable
- Explainable
- Repeatable
- Accurate enough for navigation experiments
- Consistent with differential-drive assumptions

Further tuning would mostly mean chasing small Gazebo contact-solver effects rather than improving the robot model meaningfully.

Therefore:

`drive collision width = 0.005 m`

was selected as the final value.

---

# 37. Important Failed Hypotheses

Several hypotheses were investigated and rejected or weakened.

## Wheel radius

Weak hypothesis because straight-line motion was already accurate.

## Wheel separation

Not changed because pure rotation demonstrated correct angular motion with `0.60 m`.

## Caster friction

Changed behavior but did not solve the underlying problem physically.

## Caster trail

Affected contact behavior but did not remove the systematic drift magnitude.

## Old fixed caster

Strong contributor to unrealistic turning because it could not swivel.

Replacing it with a swivel caster was physically justified.

## Center of mass

A real stability problem.

Moving the COM forward solved the robot's backward tipping.

## Drive-wheel collision width

Strong experimental effect.

Reducing it systematically reduced pure-rotation translation and curved-motion error.

---

# 38. Experimental Thinking Learned

A major lesson was the difference between correlation and proof.

At several points, two numbers appeared to match.

That was not enough to conclude causation.

The correct process was:

1. Observe a pattern.
2. Form a hypothesis.
3. Predict what should happen if the hypothesis is correct.
4. Change one variable.
5. Run the experiment.
6. Measure the result.
7. Accept, reject, or refine the hypothesis.

This prevented random parameter tuning.

---

# 39. Odometry vs Ground Truth

I learned that `/odom` is an estimate produced from wheel motion.

It is not automatically ground truth.

The robot can have:

`/odom = mathematically correct`

while:

`physical Gazebo motion = different`

because the physical model includes:

- Contact forces
- Friction
- Caster forces
- Center of mass
- Collision geometry
- Wheel-ground interaction

Therefore odometry must be validated against an independent motion source.

---

# 40. Physical Meaning of Calibration

Calibration is not simply changing a number until the output looks correct.

Calibration means:

- Identify the error
- Find the likely physical cause
- Design a controlled test
- Measure actual behavior
- Compare prediction against observation
- Correct the model
- Repeat the test

The purpose is to understand why the robot behaves incorrectly.

---

# 41. Git Repository Recovery

During this work, the main repository:

`~/mission-korea`

stopped being recognized as a Git repository.

Running:

`git status`

returned:

`fatal: not a git repository`

Investigation showed that the `.git` directory was missing.

The project files themselves were still present.

A clean copy of the Git metadata was recovered from GitHub and copied back into:

`~/mission-korea/.git`

Initially Git showed almost every tracked file as deleted while identical files appeared as untracked.

The reason was that the recovered clone used an empty/no-checkout index.

The Git index was repaired using:

`git reset --mixed HEAD`

After this, Git correctly showed only the real modified files.

This recovered the repository without overwriting the current robotics work.

---

# 42. Git Safety Lesson

During repository recovery I avoided dangerous commands such as:

`git reset --hard`

`git clean -fd`

`git restore .`

because they could have destroyed uncommitted calibration work.

Important lesson:

When Git metadata is damaged, protect the working files first.

Do not use destructive Git commands until the repository state is understood.

---

# 43. Main Lessons Learned

1. Correct equations do not guarantee correct physical simulation.

2. Odometry is an estimate, not ground truth.

3. Straight motion, pure rotation, and curved motion should be tested separately.

4. Wheel radius mainly affects travelled distance.

5. Wheel separation strongly affects turning calculations.

6. Physical contact geometry can change effective differential-drive behavior.

7. A fixed caster can create unrealistic sideways forces.

8. A passive swivel caster better represents the real robot.

9. Center-of-mass placement affects robot stability and contact loading.

10. The COM must remain inside the support polygon.

11. Visual geometry and collision geometry have different purposes.

12. Finite wheel collision width can introduce contact-point uncertainty.

13. Calibration must change one independent variable at a time.

14. Numerical coincidence is not experimental proof.

15. Fresh simulation runs are important for repeatability tests.

16. Contact physics can create small run-to-run variation.

17. Calibration should stop when error becomes small, repeatable, and explainable.

18. Failed hypotheses are useful because they narrow the search space.

19. Physics debugging can take much longer than writing code.

20. A day with little or no new code can still contain important robotics research work.

---

# 44. Learning Evidence

During this investigation I:

- Compared ROS2 odometry against independent Gazebo ground truth
- Calculated body-frame forward and sideways velocity
- Calculated ground-truth angular velocity
- Fixed timestamp handling in the diagnostic
- Investigated systematic and contact-related errors
- Tested wheel radius reasoning
- Tested wheel-separation reasoning
- Investigated fixed-caster scrubbing
- Rebuilt the robot with a passive swivel caster
- Diagnosed robot tipping
- Learned the support-polygon concept
- Corrected center-of-mass placement
- Corrected the chassis inertial model
- Tested caster trail
- Tested multiple drive-wheel collision widths
- Predicted experimental results before testing
- Performed repeatability testing
- Tested positive and negative curved motion
- Reduced pure-rotation translation
- Validated the final differential-drive physical model
- Recovered the Git repository without losing current work

---

# 45. Final Result

The robot now has a stable and experimentally validated physical model.

Final parameters:

`wheel radius = 0.10 m`

`wheel separation = 0.60 m`

`drive collision width = 0.005 m`

`caster trail = 0.02 m`

`base COM x = +0.05 m`

The custom odometry and Gazebo ground truth now agree closely during:

- Straight motion
- Pure rotation
- Left curves
- Right curves

The remaining error is small enough to continue toward higher-level localization, SLAM, and navigation work.

---

# Resume Point

Experimentally investigated and calibrated a ROS2/Gazebo differential-drive mobile robot by comparing custom wheel-encoder odometry against independent simulator ground truth.

Diagnosed fixed-caster scrubbing, center-of-mass instability, caster geometry, wheel-contact effects, and finite collision-width behavior.

Rebuilt the robot with a passive swivel caster, stabilized the chassis using corrected COM placement, and reduced turning-related simulation error through controlled parameter experiments and repeatability testing.

Final curved-motion angular variation was approximately within ±0.84%, with nearly exact forward velocity and very small lateral motion.
EOF
