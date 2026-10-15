Day 65 — Humanoid Leg Forward Kinematics: Derivation, Python, and Validation
Date: 2026-10-15
Mission: Mission Robotics 2028 — preparation for a funded research Master's
Main research direction: Legged humanoid robotics, ultimately locomotion and kitchen/service manipulation
Project: projects/humanoid-robot/kinematics/
Implementation: projects/humanoid-robot/kinematics/two_link_leg.py
Status: First 2D forward-kinematics implementation and visualization working; refactoring and systematic tests remain.
Today's goal
Derive and implement forward kinematics for a two-link humanoid leg without copying a finished solution. Use basic trigonometry to calculate hip-to-knee and hip-to-foot geometry, check physical consistency, then visualize the links in Python.
This is an initial geometric model. It is not yet a walking, balanced, or dynamics-controlled humanoid.
Why this matters to the humanoid project
A legged robot must know where its feet are relative to its body. Forward kinematics answers:
Given the link lengths and joint angles, where are the knee and foot?

The current model will later support inverse kinematics, joint control, foot placement, balance experiments, and eventually 3D articulated humanoid simulation.
The earlier wheeled-robot ROS2, Gazebo, odometry, coordinate-frame, and experimental work remains useful, but the primary project has shifted to legged humanoid robotics.
1. Physical model and coordinate convention
Two rigid links in a 2D X–Z plane:
             +Z (up)
              ^
              |
  -X <-------- HIP (0, 0) --------> +X (forward)
                \
                 \  L1 = thigh
                  KNEE
                     \
                      \  L2 = shin
                       FOOT / shin endpoint
              |
              v -Z (down)
Symbol	Meaning	Initial value
L1	Thigh length, hip to knee	0.4 m
L2	Shin length, knee to foot endpoint	0.4 m
θ1	Hip angle measured from vertically downward	varied
θ2	Knee angle relative to the thigh	varied
(x, z)	Location in the hip-centered frame	metres


Conventions used in this lesson: Hip origin (0, 0), +X forward, +Z up. At θ1 = 0, the thigh points down. Positive angle turns a link toward +X. The shin's angle measured from downward vertical is θ1 + θ2.
Limits of the model: We use a point at the shin endpoint as the “foot.” We have no ankle joint, physical foot geometry, toe direction, joint limits, masses, torques, ground forces, or 3D side-to-side motion yet.
2. Mathematical derivation
First link: Hip → Knee
Since hip angle is measured from downward vertical:
\[
x_{knee} = L_1\sin(\theta_1)
\]
\[
z_{knee} = -L_1\cos(\theta_1)
\]
The negative sign on Z is necessary because the knee is below the hip for an approximately downward-pointing thigh.
Second link: Knee → Foot
The knee joint is relative to the thigh, not the world. Therefore:
\[
\theta_{shin} = \theta_1 + \theta_2
\]
\[
\Delta x_{shin} = L_2\sin(\theta_1 + \theta_2)
\]
\[
\Delta z_{shin} = -L_2\cos(\theta_1 + \theta_2)
\]
Complete forward kinematics: Hip → Foot
\[
\boxed{x_{foot} = L_1\sin(\theta_1) + L_2\sin(\theta_1 + \theta_2)}
\]
\[
\boxed{z_{foot} = -L_1\cos(\theta_1) - L_2\cos(\theta_1 + \theta_2)}
\]
Unit discipline: Angles can be described in degrees during planning, but Python's math.sin() and math.cos() require radians, so convert with math.radians() before calling the function.
3. Link lengths versus direct distance
Two different quantities must not be confused:
1. Distance following the rigid links: L1 + L2 = 0.8 m. It does not change when joints rotate.
2. Direct hip-to-foot distance: changes with joint angles. Because the hip is at the origin:
\[
d_{hip,foot} = \sqrt{x_{foot}^2+z_{foot}^2}
\]
The direct distance is never greater than L1 + L2. For an extended leg it equals 0.8 m; when a knee bends it is usually less.
For an arbitrary (nonzero) hip position, calculate the distance using coordinate differences rather than simply sqrt(x_foot² + z_foot²).
Also learned: a coordinate being negative indicates position relative to a frame, not backward or downward velocity. Position and orientation are different; without an ankle/foot model, we know shin orientation but not which way the toes point.
4. Numerical configurations tested
All examples use L1 = L2 = 0.4 m and the conventions above. Values rounded to four decimal places unless shown otherwise.
Hip θ1	Knee θ2	Knee (x, z), m	Foot (x, z), m	Direct hip–foot distance
30°	+20°	(0.2000, −0.3464)	(0.5064, −0.6035)	≈ 0.788 m
0°	0°	(0.0000, −0.4000)	(0.0000, −0.8000)	0.8000 m
0°	+90°	(0.0000, −0.4000)	(0.4000, −0.4000)	0.5656854249492381 m
30°	−60°	(0.2000, −0.3464)	(0.0000, −0.6928)	≈ 0.6928 m
30°	−30°	(0.2000, −0.3464)	(0.2000, −0.7464)	0.7727406610312547 m


Insights from the experiments:
- 30° + (-60°) = -30°: the shin returns toward −X as the thigh extends toward +X. With equal link lengths, opposing horizontal displacements cancel and the foot's X position returns to 0.
- 30° + (-30°) = 0°: the shin points straight downward. The knee and foot share the same X coordinate (0.2 m), although their Z coordinates differ.
- 0° / 90°: thigh vertical, shin horizontal, so hip–knee–foot form a right triangle. The direct distance is sqrt(0.4² + 0.4²) ≈ 0.5657 m.
- The equal link lengths do not imply all straight-line hip-to-foot distances equal 0.8 m; that occurs only when both links are aligned.
5. Python implementation progress
Created the new project directory and implemented:
projects/humanoid-robot/kinematics/two_link_leg.py
Skills practised:
- Importing math and matplotlib.pyplot.
- Writing numeric measurements without suffixes such as 0.4 m (which is invalid Python); placing units in comments instead.
- Converting degrees to radians with math.radians().
- Calculating knee and foot X/Z coordinates using sine and cosine.
- Using math.sqrt() to calculate direct distance.
- Creating paired plotting coordinate lists in the order hip → knee → foot.
- Plotting with plt.plot(..., marker="o") and displaying with plt.show().
- Setting plt.axis("equal") so 0.4 m on X and 0.4 m on Z appear equally long.
- Defining forward_kinematics(thigh_length, shin_length, hip_angle, knee_angle).
- Passing different joint configurations as function arguments.
- Returning (knee_x, knee_z, foot_x, foot_z) and using tuple unpacking in the calling code.
- Formatting printed values with :.2f.
The mathematical core implemented by the learner is:
knee_x = thigh_length * math.sin(hip_angle)
knee_z = thigh_length * -math.cos(hip_angle)

shin_angle = hip_angle + knee_angle
foot_x = knee_x + shin_length * math.sin(shin_angle)
foot_z = knee_z - shin_length * math.cos(shin_angle)

return knee_x, knee_z, foot_x, foot_z
The actual script in projects/humanoid-robot/kinematics/two_link_leg.py is the authoritative source. Do not replace that script with this excerpt; it omits plotting and calling code on purpose.
Last confirmed execution
Parameters: hip = 0°, knee = 90°, thigh = 0.4 m, shin = 0.4 m.
0.0
1.5707963267948966
knee_x: 0.0, knee_z: -0.4
foot_x: 0.4, foot_z: -0.4
straight_line_distance: 0.5656854249492381
[0, 0.0, 0.4]
[0, -0.4, -0.4]
Knee Cordinates: (0.00, -0.40) | Foot Coordinates: (0.40, -0.40)
The Matplotlib window opens and shows an L-shaped leg, then terminal output appears after closing the window because plt.show() is blocking in the current setup.
6. Mistakes found and corrected
Mistake	Reason	Correction / lesson
Wrote 0.4 m in Python	Python does not parse a physical unit after a number	Use 0.4  # meters
Unexpected top-level indentation	Python blocks depend on indentation	Keep top-level statements unindented
Initial knee Z was positive	Coordinate convention is +Z upward	Knee Z needs -L1 * cos(θ1)
Used shin_length for knee Z	Confused which link determines knee position	Both knee coordinates depend on thigh_length
Forgot square root and reported squared distance (~0.16)	Confused d² with d	Use sqrt(x² + z²)
Plot list originally skipped hip	Would draw only the shin segment	Plot three points: hip, knee, foot
Named vertical values y_positions	Inconsistent with chosen X–Z robot plane	Use z_positions
marker="0" in Matplotlib	Digit zero is not the desired circle marker	Use lowercase letter o
Function overwrote arguments / read global angles	Function couldn't truly handle arbitrary inputs	Use the function's own thigh_length, shin_length, hip_angle, knee_angle parameters
Function defined but not called	Definition alone does not run a function	Call it and pass arguments
NameError from similar angle variable names	...radius, ...radians, hip_angle are distinct names	Keep names consistent; check traceback


Research habit learned: A script can run and even give a correct number for one case while hiding a logic error. Changing link lengths and angles is an important validation technique.
7. What has been demonstrated — and what has not
Demonstrated today: Basic 2D kinematics derivation, working Python numerical calculation, hand-verification for selected configurations, correct plotting, passing parameters into a function, and returning coordinates.
Not demonstrated yet: Comprehensive automated tests, arbitrary hip offset, independent plotting/math modules, inverse kinematics, Jacobians, joint velocity, torque/control, robot balance, foot-ground contact, 3D kinematics, or a Gazebo biped.
Current coding state at the stopping point: The working forward_kinematics() function still contains Matplotlib plotting and print statements. It returns four coordinates, but the planned refactor to move plotting out of the function has not been completed. The plotting coordinate lists still reference global x_hip and z_hip. Do not record this refactor as finished.
8. Learning Evidence
- Source file: [`two_link_leg.py`](../../../projects/humanoid-robot/kinematics/two_link_leg.py) — original Python implementation created during the lesson.
- Screenshot: [0° hip / 90° knee — plot and terminal](evidence/leg-0deg-90deg.png) — learner-provided screenshot of the current leg visualization and terminal output.
- Numerical evidence: terminal results in section 5, particularly straight_line_distance: 0.5656854249492381.
- Debugging evidence: learner resolved errors in units, signs, indentation, parameter names, missing function call, and plot marker.
No video was recorded or supplied for this session; do not fabricate a YouTube evidence link.
9. Professor-style reflection
Strength: I moved from interpreting the equations to implementing them, debugging the code, predicting leg positions, and comparing visual/numerical results. I correctly understood that knee bending changes direct hip-to-foot distance without changing the rigid link lengths.
Main weakness to improve: Code organization and parameter independence needed repeated revisions. Future functions should avoid dependence on unrelated global values. I should test more than one configuration and check physical invariants, not merely accept a result because Python runs.
Scope of achievement: This is a first working subsystem, not evidence that a humanoid can balance or walk. The next improvements should be small and independently implemented.
10. Exact resume point for next study session
Do not redo the trigonometry lesson. Pick up from the working two_link_leg.py.
1. Move the plotting coordinate lists and Matplotlib calls outside forward_kinematics(), below the function call and tuple unpacking. Confirm the picture still matches.
2. Move the remaining printing outside the mathematical function, so the function's job is to compute and return geometry.
3. Validate at least three known cases and link-length invariants; then begin basic automated tests.
4. Only after refactoring/testing, introduce inverse kinematics (desired foot location → possible joint angles).
Stopping checkpoint: Both 2D links are rendered at equal scale; the 0°/90° case returns correct coordinates and distance. The return statement and tuple unpacking work. Refactoring is the next task.
