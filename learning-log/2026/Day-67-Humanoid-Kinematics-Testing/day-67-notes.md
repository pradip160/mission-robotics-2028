
import math

hip_angle = math.radians(30)

print(hip_angle)
math.atan2(y, x)
Mission Korea 2028 — Day 67 Learning Log

Date: 17 October 2026
Project: Humanoid Robot — 2D Two-Link Leg
Topic: Forward Kinematics Verification, Python Debugging, and Introduction to Inverse Kinematics
Status: Day 67 complete — forward-kinematics tests passed; inverse kinematics studied on paper, not yet implemented.
1. Today's objectives and outcome

Today's practical objective was to strengthen my two-link forward-kinematics program by testing expected foot coordinates and then reusing the function for different joint angles and link lengths. I also studied the mathematics of inverse kinematics (IK) for the first time.

Completed:

    Added two positional assertions for a leg with hip angle 0° and knee angle 90°.
    Verified a second configuration with both angles at 0° (fully extended downward leg).
    Verified a third configuration with unequal link lengths (0.5 m thigh, 0.3 m shin).
    Practised distinguishing function inputs from returned outputs.
    Investigated an AssertionError and corrected mistakes in function arguments, coordinate variables, signs, and tolerance notation.
    Reviewed trigonometry, 2D coordinates, link distances, reachability, and the analytical two-link IK equations.

Not yet completed: Python implementation or testing of inverse kinematics.
2. Robot model and coordinate conventions

We use an ideal two-link leg moving in a 2D x–z plane:

    Hip is at (0, 0).
    +x is forward/right; +z is upward; −z is downward.
    L1 is thigh length and L2 is shin length, in metres.
    theta1 is the hip angle, measured from the downward vertical. A hip angle of 0° means the thigh points straight down; positive values rotate it forward.
    theta2 is the knee angle relative to the thigh.
    The shin's angle relative to downward vertical is theta1 + theta2.
    Trigonometric functions in Python use radians.

For this simplified model, ignore joint stops, collisions, foot orientation, body motion, and balance unless specifically added later.
Symbol	Description
L1, L2	Thigh and shin lengths (m)
theta1, theta2	Hip and relative knee angles (radians in code)
(knee_x, knee_z)	Knee coordinates relative to hip
(foot_x, foot_z)	Foot coordinates relative to hip
d	Direct hip-to-foot distance (m)
3. Essential mathematics — forward kinematics
Basic trigonometry

For a right triangle:

    sin(theta) = opposite / hypotenuse
    cos(theta) = adjacent / hypotenuse
    theta_radians = theta_degrees × pi / 180
    theta_degrees = theta_radians × 180 / pi

Knee position
knee_x = L1 × sin(theta1)
knee_z = −L1 × cos(theta1)
Shin direction
shin_angle = theta1 + theta2
Foot position
foot_x = knee_x + L2 × sin(theta1 + theta2)
foot_z = knee_z − L2 × cos(theta1 + theta2)

Combining these gives the complete forward-kinematics equations:
foot_x = L1 × sin(theta1) + L2 × sin(theta1 + theta2)
foot_z = −L1 × cos(theta1) − L2 × cos(theta1 + theta2)

Mental model: Joint angles and link lengths → knee and foot coordinates.
Distances and geometric invariants

For two positions (x1, z1) and (x2, z2):
distance = sqrt((x2 − x1)^2 + (z2 − z1)^2)

Therefore:
calculated_thigh_length = sqrt((knee_x − hip_x)^2 + (knee_z − hip_z)^2)
calculated_shin_length  = sqrt((foot_x − knee_x)^2 + (foot_z − knee_z)^2)

These should equal L1 and L2 respectively. With the hip at the origin:
d_hip_to_foot = sqrt(foot_x^2 + foot_z^2)

Important distinction: Distance along the links is always L1 + L2, but the straight-line distance from hip to foot varies as the leg bends.
4. My Python implementation

The reusable function built in this project is:
import math

def forward_kinematics(thigh_length, shin_length, hip_angle, knee_angle):
    knee_x = thigh_length * math.sin(hip_angle)
    knee_z = -thigh_length * math.cos(hip_angle)

    shin_angle = hip_angle + knee_angle

    foot_x = knee_x + shin_length * math.sin(shin_angle)
    foot_z = knee_z - shin_length * math.cos(shin_angle)

    return knee_x, knee_z, foot_x, foot_z

Function inputs: thigh_length, shin_length, hip_angle, knee_angle.
Function outputs: knee_x, knee_z, foot_x, foot_z.

When calling a function, values inside parentheses are inputs, and names on the left side of = receive its outputs.
5. Three configurations tested today
Test	Thigh L1	Shin L2	Hip	Knee	Expected foot (x, z)	Observed result
A — Bent leg	0.4 m	0.4 m	0°	90°	(0.4, −0.4) m	Passed
B — Straight leg	0.4 m	0.4 m	0°	0°	(0.0, −0.8) m	Passed
C — Unequal links	0.5 m	0.3 m	0°	90°	(0.3, −0.5) m	Passed
Test A — Original bent configuration

    Knee = (0.0, −0.4) m.
    Foot = (0.4, −0.4) m.
    Direct hip-to-foot distance = sqrt(0.4² + (−0.4)²) ≈ 0.5656854249 m.
    Both link lengths were validated with math.isclose().
    New positional assertions verified foot_x ≈ 0.4 and foot_z ≈ −0.4.

Test B — Fully extended downward leg

    Input angles: hip = 0°, knee = 0°.
    Expected foot = (0.0, −0.8) m.
    Additional function call stored outputs under straight_... names, leaving the original results untouched.

Test C — Unequal link lengths

    Inputs: thigh = 0.5 m, shin = 0.3 m, hip = 0°, knee = 90°.
    Expected knee = (0.0, −0.5) m.
    Expected foot = (0.3, −0.5) m.
    This test checks that the formulas genuinely use the correct link-length parameters, not just two equal lengths.

Compact reference — tests that were verified

The following is a consolidated reference of the three test calls and assertions, rather than a verbatim copy of my entire local script:
# A. Original bent leg
knee_x, knee_z, foot_x, foot_z = forward_kinematics(
    0.4, 0.4, math.radians(0), math.radians(90)
)

calculated_thigh_length = math.sqrt(knee_x**2 + knee_z**2)
calculated_shin_length = math.sqrt(
    (foot_x - knee_x)**2 + (foot_z - knee_z)**2
)

assert math.isclose(calculated_thigh_length, 0.4, abs_tol=1e-9)
assert math.isclose(calculated_shin_length, 0.4, abs_tol=1e-9)
assert math.isclose(foot_x, 0.4, abs_tol=1e-9)
assert math.isclose(foot_z, -0.4, abs_tol=1e-9)

# B. Fully extended leg
straight_knee_x, straight_knee_z, straight_foot_x, straight_foot_z = forward_kinematics(
    0.4, 0.4, math.radians(0), math.radians(0)
)
assert math.isclose(straight_foot_x, 0.0, abs_tol=1e-9)
assert math.isclose(straight_foot_z, -0.8, abs_tol=1e-9)

# C. Unequal links
unequal_knee_x, unequal_knee_z, unequal_foot_x, unequal_foot_z = forward_kinematics(
    0.5, 0.3, math.radians(0), math.radians(90)
)
assert math.isclose(unequal_foot_x, 0.3, abs_tol=1e-9)
assert math.isclose(unequal_foot_z, -0.5, abs_tol=1e-9)

Terminal evidence from my final run:
Knee Cordinates: (0.00, -0.40) | Foot Coordinates: (0.40, -0.40)
hip_angle_in_radians: 0.0
knee_angle_in_radians: 1.5707963267948966
Calculated thigh length: 0.4
knee_x: 0.0, knee_z: -0.4
foot_x: 0.4, foot_z: -0.4
straight_line_distance: 0.5656854249492381
straight_foot_x: 0.0, straight_foot_z: -0.8
Unequal leg foot: (0.3, -0.5)

The run ended normally without an AssertionError. The displayed Matplotlib plot still represented Test A because plotting used the original knee_x, knee_z, foot_x, and foot_z variables. That is expected, not a bug.
6. Debugging lessons from today
Mistake 1 — Confusing inputs and outputs

I initially tried to pass straight_foot_x, straight_foot_z, etc. into forward_kinematics(). Those are output coordinates that the function is supposed to calculate. The function needs the two lengths and two angles as inputs.
Mistake 2 — Reusing angles from the wrong configuration

Using the original hip_angle_in_radians and knee_angle_in_radians repeated the (0°, 90°) experiment rather than testing (0°, 0°). Variable names do not determine the robot's physical configuration; argument values do.
Mistake 3 — Putting link lengths inside math.radians()

math.radians(0.5) means half a degree, not a thigh length of half a metre. Pass lengths as numbers and convert only angular values.
Mistake 4 — Changing shared/global link-length variables

Changing thigh_length and shin_length globally from (0.4, 0.4) to (0.5, 0.3) also changes the earlier test that expects (0.4, −0.4). Instead, provide 0.5, 0.3 directly in the separate third call (or use clearly separated named parameters).
Mistake 5 — Checking the knee while expecting the foot

The first unequal-length attempt contained:
assert math.isclose(unequal_knee_x, 0.3, abs_tol=1e-9)

That assertion failed because for (hip=0°, knee=90°), knee_x = 0, while foot_x = 0.3. Always distinguish the joint position being tested.
Mistake 6 — Wrong vertical sign

With the hip at the origin and +z pointing upward, the knee and foot below the hip have negative z values. For the unequal-length test, the expected foot is (0.3, −0.5), not (0.3, +0.5).
Mistake 7 — Typing 12-9 instead of 1e-9
abs_tol=12-9   # WRONG: Python evaluates this as 3
abs_tol=1e-9   # CORRECT: 0.000000001

A tolerance of 3 m is too loose for this small robot and can hide serious errors.
Testing principle

    Geometric invariant tests check whether the links retain their lengths.
    Known-position tests check whether the foot reaches the right coordinates for specific inputs.
    Both are useful, but neither proves correctness for every joint angle, every link length, or all physical joint constraints.

7. New theory: Inverse kinematics (IK)

Forward kinematics: link lengths + joint angles → foot coordinates.
Inverse kinematics: link lengths + desired foot coordinates → required joint angles.

An IK solver must first check whether the target is reachable.
7.1 Reachability

For hip at the origin and target (x, z):
d = sqrt(x² + z²)
d_max = L1 + L2
d_min = abs(L1 − L2)

A target is geometrically reachable in this ideal unrestricted planar two-link model if:
abs(L1 − L2) ≤ d ≤ L1 + L2

Example — L1 = 0.5 m, L2 = 0.3 m
d_min = |0.5 − 0.3| = 0.2 m
d_max = 0.5 + 0.3 = 0.8 m

    Target (0.3, −0.5): d = sqrt(0.34) ≈ 0.5831 m → reachable geometrically.
    Target (0.6, −0.6): d = sqrt(0.72) ≈ 0.8485 m → unreachable, because 0.8485 > 0.8.
    Target (0, −0.1): d = 0.1 m → unreachable, because 0.1 < 0.2.

Actual robots also have joint angle limits, obstacles, and collisions. Passing this reach test is necessary but not always sufficient for physical reachability.
7.2 Law of cosines

For a triangle:
c² = a² + b² − 2ab × cos(C)

For our specific knee-angle convention, the relation is:
d² = L1² + L2² + 2 L1 L2 × cos(theta2)

Hence:
C = (x² + z² − L1² − L2²) / (2 L1 L2)
theta2 = ± acos(C)

Here, acos means inverse cosine. For a reachable target, C should lie between −1 and +1 (allowing for small floating-point errors). The positive/negative options represent different knee-bending configurations.
7.3 Hip angle

Once we choose a knee-angle solution theta2, the hip angle is:
theta1 = atan2(x, −z)
         − atan2(L2 × sin(theta2), L1 + L2 × cos(theta2))

atan2(y, x) returns an angle with correct directional quadrant information. In the first term above, atan2(x, −z) is intentional: our zero-angle axis points down, not right.
7.4 Analytical IK example

For L1 = 0.4 m, L2 = 0.4 m, and target foot (x, z) = (0.4, −0.4):
d² = 0.4² + (−0.4)² = 0.32
C  = (0.32 − 0.16 − 0.16) / (2 × 0.4 × 0.4) = 0
theta2 = ± acos(0) = ± 90°

One solution:
theta2 = +90°
theta1 = atan2(0.4, 0.4) − atan2(0.4, 0.4)
       = 45° − 45° = 0°

Another geometrical solution:
theta2 = −90°
theta1 = +90°

Both place the foot at (0.4, −0.4) in the ideal model. A real robot's joint limits can rule out one or both solutions.

Important: We only studied these IK equations today. We did not yet write or verify an IK function in Python.
8. Notebook-ready formula sheet
ANGLES
  radians = degrees × pi / 180
  degrees = radians × 180 / pi

FORWARD KINEMATICS
  knee_x = L1 sin(theta1)
  knee_z = −L1 cos(theta1)
  shin_angle = theta1 + theta2
  foot_x = L1 sin(theta1) + L2 sin(theta1 + theta2)
  foot_z = −L1 cos(theta1) − L2 cos(theta1 + theta2)

DISTANCES
  distance(A, B) = sqrt((xB − xA)² + (zB − zA)²)
  hip_to_foot_d = sqrt(foot_x² + foot_z²)   [hip at origin]

INVERSE KINEMATICS (IDEAL PLANAR TWO-LINK MODEL)
  d_min = abs(L1 − L2)
  d_max = L1 + L2
  reachable if d_min ≤ sqrt(x² + z²) ≤ d_max
  C = (x² + z² − L1² − L2²) / (2 L1 L2)
  theta2 = ± acos(C)
  theta1 = atan2(x, −z) − atan2(L2 sin(theta2), L1 + L2 cos(theta2))

These formulas assume positive nonzero link lengths and the coordinate convention stated above. Angles in code are radians.
9. Exactly where to resume — Day 68

Current local project file:
~/mission-korea/projects/humanoid-robot/kinematics/two_link_leg.py

Current verified state: The forward-kinematics function, first configuration plot, and three configuration tests ran successfully. Leave these tests in place.

Next lesson: Begin implementing two-link inverse kinematics step by step, rather than copying a complete solution:

    Start from desired foot coordinates (x, z) and link lengths L1, L2.
    Calculate the direct distance d = sqrt(x² + z²).
    Compare d with abs(L1 − L2) and L1 + L2.
    Test reachable and unreachable examples before calculating knee or hip angles.
    Only after reachability works, derive and implement theta2; then theta1; then check IK by feeding the angles back through the existing FK function.

First Day 68 programming checkpoint: Independently write a small reachability check for L1=0.5, L2=0.3, target (0.6, −0.6). Explain why it must reject that target. Do not implement the full IK solver in one jump.

Long-term context: This is basic 2D kinematics for the eventual humanoid/legged-robotics research goal. IK gives joint configurations; it does not itself guarantee balance, stable ground contact, actuator feasibility, or dynamic control.

End of Day 67 — Mission Korea 2028.
