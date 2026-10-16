Day 66 — Humanoid Robot: Reusable Forward Kinematics and Geometry Tests
Date: 16 October 2026
Mission: Mission Korea 2028 — Funded Master's preparation in robotics
Main project: Legged humanoid robot (long-term goal: walking, manipulation, and kitchen tasks)
Today's working file: projects/humanoid-robot/kinematics/two_link_leg.py
Status: Today's study session completed; known-position assertions are for Day 67.
1. Today's Objective
Improve yesterday's working two-link leg program so that:
1. Forward kinematics is a reusable mathematical function.
2. Printing and Matplotlib plotting happen outside the function.
3. The returned coordinates can be checked against physical constraints using automated assertions.
I continued from Day 65; I did not start a new leg model or move to inverse kinematics today.
2. Robot Model and Coordinate Convention
Our simplified leg is a 2D, two-link model, with the hip at the origin:
- Hip: (x_hip, z_hip) = (0, 0)
- Thigh length: L1 = 0.4 m
- Shin length: L2 = 0.4 m
- Hip angle: θ1 = 0°
- Knee angle: θ2 = 90° (relative to the thigh)
- +X points forward and +Z points upward.
- Positive joint angles rotate a link toward the forward direction according to our chosen convention.
The shin's direction in this frame is θ1 + θ2.
Forward-kinematics equations
For the knee (relative to the hip):
\[
x_{knee} = L_1\sin(\theta_1)
\]
\[
z_{knee} = -L_1\cos(\theta_1)
\]
For the foot (relative to the hip):
\[
x_{foot} = x_{knee} + L_2\sin(\theta_1 + \theta_2)
\]
\[
z_{foot} = z_{knee} - L_2\cos(\theta_1 + \theta_2)
\]
Python's math.sin() and math.cos() use radians. The input angles were converted with math.radians(0) and math.radians(90).
Expected and observed configuration
Joint	X (m)	Z (m)
Hip	0.0	0.0
Knee	0.0	-0.4
Foot	0.4	-0.4


The straight-line hip-to-foot distance is:
\[
d_{hip\to foot} = \sqrt{0.4^2+(-0.4)^2} \approx 0.565685\ \text{m}
\]
Reminder: The physical path along the thigh and shin totals 0.8 m, but the straight-line hip-to-foot distance is shorter when the knee bends.
3. Work Completed Today
A. Separated visualization from forward kinematics
At first, forward_kinematics() contained both calculations and plt.plot(), plt.axis("equal"), and plt.show().
I moved the coordinate lists and Matplotlib statements outside the function, after the function call returned the four joint coordinates. The function now focuses on calculating and returning positions:
def forward_kinematics(thigh_length, shin_length, hip_angle, knee_angle):
    knee_x = thigh_length * math.sin(hip_angle)
    knee_z = -thigh_length * math.cos(hip_angle)

    shin_angle = hip_angle + knee_angle
    foot_x = knee_x + shin_length * math.sin(shin_angle)
    foot_z = knee_z - shin_length * math.cos(shin_angle)

    return knee_x, knee_z, foot_x, foot_z
This excerpt documents the mathematical part I implemented. My full working file also contains input parameters, plotting, and print statements outside the function.
Why this matters: A robot controller may need to call forward kinematics many times. It should receive coordinates without repeatedly opening a graph window.
B. Used returned values outside the function
I used tuple unpacking:
knee_x, knee_z, foot_x, foot_z = forward_kinematics(
    thigh_length,
    shin_length,
    hip_angle_in_radians,
    knee_angle_in_radians,
)
I initially worried that calculating the thigh length outside the function would cause a NameError. I learned that the variables created inside the function are local, but the return statement sends their values to variables assigned outside the function. That is why I can plot and test the returned coordinates in the main script.
C. Understood Matplotlib's blocking behavior
When plt.show() came before the print statements, the final terminal output appeared only after I closed the plot window. I moved plt.show() below the print statements.
Observed result: Terminal output appeared before/while the plot was visible, and the 2D leg visualization continued to work. This was expected Python execution order, not a kinematics error.
D. Removed an unnecessary calculation from the function
I had calculated straight_line_distance both inside and outside forward_kinematics() even though the function did not return or use it. I removed the unused calculation inside the function and kept the distance calculation outside.
E. Added a thigh-length geometry check
The distance from hip to knee must equal the thigh's rigid physical length, regardless of joint angle:
\[
L_{1,calc}=\sqrt{(x_{knee}-x_{hip})^2+(z_{knee}-z_{hip})^2}
\]
My Python calculation (outside the function) was:
calculated_thigh_length = math.sqrt(
    (knee_x - x_hip)**2 + (knee_z - z_hip)**2
)
The terminal printed Calculated thigh length: 0.4.
F. Learned assert and math.isclose()
- assert checks that a condition is true; if false, Python raises AssertionError.
- math.isclose(a, b) compares floating-point values within a tolerance, avoiding fragile exact-equality checks.
- A passing assert is normally silent.
My first test was:
assert math.isclose(calculated_thigh_length, thigh_length)
Deliberate failure experiment: I changed the expected value to 0.5:
assert math.isclose(calculated_thigh_length, 0.5)
Python raised the expected AssertionError at that line, confirming the assertion can detect a wrong expected length. I then restored the comparison against thigh_length.
G. Added a shin-length geometry check
The distance from knee to foot must equal the fixed shin length:
\[
L_{2,calc}=\sqrt{(x_{foot}-x_{knee})^2+(z_{foot}-z_{knee})^2}
\]
I implemented:
calculated_shin_length = math.sqrt(
    (foot_x - knee_x)**2 + (foot_z - knee_z)**2
)

assert math.isclose(calculated_thigh_length, thigh_length)
assert math.isclose(calculated_shin_length, shin_length)
Observed result: Both assertions passed for the tested 0° / 90° joint configuration, and the Matplotlib visualization still displayed the expected shape.
4. Bugs and Debugging Lessons
Problem 1 — Using coordinate lists before they existed: After moving x_positions and z_positions outside the function, I temporarily left print statements referring to those names inside the function. Because the lists had not been created when the function was called, the code would raise NameError. Fix: Remove those prints from inside the function; create/use lists after calling it.
Problem 2 — Variable-name typo: I got:
NameError: name 'knee_x' is not defined. Did you mean: 'kee_x'?
The name was inconsistent at the receiving/calculation point. I corrected it and successfully reran the distance calculation. Lesson: Variable names must match exactly; this error was about Python naming, not kinematics.
Problem 3 — Assertion failure: Python raised AssertionError when I deliberately compared the calculated 0.4 m thigh against 0.5 m. Lesson: A deliberately failing test is useful evidence that the check can catch at least one incorrect result.
5. Verified Results and What They Mean
From the latest successful run I shared:
Knee Cordinates: (0.00, -0.40) | Foot Coordinates: (0.40, -0.40)
0.0
1.5707963267948966
Calculated thigh length: 0.4
knee_x: 0.0, knee_z: -0.4
foot_x: 0.4, foot_z: -0.4
straight_line_distance: 0.5656854249492381
I also calculated calculated_shin_length and added a passing assertion against shin_length. The latest output did not explicitly print the shin length, but the program continued without an assertion failure.
Important limitation: Passing the two link-length checks does not prove forward kinematics is always correct. A wrong joint rotation direction could still preserve both link lengths. The tests establish geometric consistency for the exercised configuration, not complete algorithm correctness.
6. Research and Programming Concepts Learned
- Separation of concerns: Keep computation distinct from printing and plotting.
- Function scope: Variables inside a function are local; returned values can be assigned and used outside it.
- Tuple unpacking: Receive (knee_x, knee_z, foot_x, foot_z) from the function.
- Execution order: plt.show() usually blocks in my interactive Matplotlib environment until the window closes.
- Physical invariants: Rigid link lengths must remain constant even when joint angles change.
- Floating-point testing: Use math.isclose() rather than assuming exact decimal equality.
- Testing limits: One correct numerical output or passing invariant is not enough to validate all robot configurations.
7. Learning Evidence
- Source: projects/humanoid-robot/kinematics/two_link_leg.py
- Evidence recorded during the session: Terminal output showing the 0° / 90° knee and foot coordinates, calculated thigh length, and hip-to-foot distance; working equal-axis Matplotlib plot.
- Assertion evidence: An intentional failing assertion against 0.5, followed by successful thigh- and shin-length assertions.
- Repository status: This note does not claim a GitHub push occurred; Git staging, committing, and pushing are handled separately.
- Video/screenshot links: Add here if captured or uploaded later.
8. Day 66 Status
- [x] Move plotting outside forward_kinematics().
- [x] Move coordinate lists outside the function.
- [x] Keep forward_kinematics() focused on computation and returning coordinates.
- [x] Move terminal output outside the function.
- [x] Understand why print order changes around plt.show().
- [x] Calculate hip-to-knee distance from returned coordinates.
- [x] Test thigh length with assert math.isclose().
- [x] Intentionally trigger an AssertionError.
- [x] Calculate knee-to-foot distance.
- [x] Test shin length with assert math.isclose().
- [ ] Add explicit expected-foot-position assertions.
- [ ] Test multiple configurations automatically.
- [ ] Start inverse kinematics.
9. Exact Resume Point — Day 67
Start with the current two_link_leg.py; do not rebuild the program.
1. For the existing hip = 0°, knee = 90°, L1 = L2 = 0.4 m configuration, add independent expected-position checks for foot_x ≈ 0.4 m and foot_z ≈ -0.4 m using math.isclose(..., abs_tol=1e-9).
2. Confirm both pass, and consider a deliberate wrong expectation to ensure they can fail.
3. Next, test additional joint-angle and unequal-link-length configurations without changing the internals of forward_kinematics().
4. Only after these tests, start introducing inverse kinematics (target foot position → required joint angles).
Next lesson rule: Work step by step; write the code myself, then request review. No full solution dumps.
Day 66 reflection: Today I moved from merely drawing a mathematically correct-looking leg to checking that its computed geometry obeys rigid-link constraints. My code still represents a simplified 2D leg; this is a foundation for future humanoid control, not yet a standing or walking humanoid.
