Loading older messages…
if knee_angle > math.radians(135)
        return None

Your logic is correct! ✅ You've chosen the right condition to enforce our humanoid robot's knee-joint limit.

There's just one Python syntax mistake: you're missing a colon (:) after the if condition.
✅ Correct code
if knee_angle > math.radians(135):
    return None

Place this immediately after:
knee_angle = math.acos(cos_knee)
🤖 Why this matters in robotics

Our hypothetical humanoid knee can bend between:
0∘≤θ2≤135∘
0∘≤θ2​≤135∘

Consider two configurations:
Calculated knee angle	Result	Reason
107.46°	✅ Accepted	Within joint limits
180°	❌ Rejected	Exceeds maximum angle

Important: Our function now checks two different constraints:

    Geometric reachability: Can the link lengths reach the target?
    Joint limits: Can the robot's knee physically rotate to the required angle?

Our current IK solver considers only one knee-bending direction and this hypothetical knee limit. More complete physical validation will come later.
🎓 Next checkpoint — Test the joint limit

Remember our previous minimum-reach experiment?
minimum_reach_result = inverse_kinematics(
    0.5,
    0.3,
    0.0,
    -0.2
)

Previously, Python returned:
(approximately 0.0, 3.141592653589793)

That represented a 180° knee bend.

Your task: Run this same experiment again after adding the joint-limit check.

What does minimum_reach_result return now, and why?

Send me your terminal result and explanation.

Continue with the joint-limit test

    Explain the returned result

type error cannnot unpack. and one questopm am  i supposed to remove the tests after we finish or what i am keeping all  until now. i mena the calling and the assertion

Good question. This is actually an important stage in your robotics programming. You're beginning to face something real software engineers encounter: when we improve a function, some older tests need to change.

Let's address both questions.
🤖 1. Why are you getting a TypeError?

Previously, your minimum-reach experiment returned:
minimum_reach_result = (0.0, 3.141592653589793)

Your code could unpack those two angles:
minimum_hip_angle, minimum_knee_angle = minimum_reach_result

But we've now introduced a mechanical knee limit:
if knee_angle > math.radians(135):
    return None

Our minimum-reach configuration requires a knee angle of:
θ2=180∘
θ2​=180∘

Since:
180∘>135∘
180∘>135∘

Your IK function correctly returns:
None

However, your old code still tries to unpack two angles:
minimum_hip_angle, minimum_knee_angle = minimum_reach_result

That's equivalent to:
minimum_hip_angle, minimum_knee_angle = None

Python cannot unpack None into two variables.

That's why you're getting a TypeError. Your IK function is behaving as intended.
How to correct the test

Previously, we expected a valid 180° knee solution.

Now, with our new joint limit, we expect rejection.

Replace your old minimum-reach assertions and their unpacking line with:
minimum_reach_result = inverse_kinematics(
    0.5,
    0.3,
    0.0,
    -0.2
)

assert minimum_reach_result is None

This verifies that our solver rejects a configuration requiring a knee angle beyond its permitted limit.
2. Should you delete your old tests?

No. Keep your tests. But we should organize them properly.

You've been keeping every function call and assertion inside:
two_link_leg.py

That's completely understandable while learning.

However, as your project grows, keeping everything in one file will become difficult to maintain.
How robotics engineers organize their code

Eventually, I recommend this structure:
mission-korea/
└── projects/
    └── humanoid-robot/
        └── kinematics/
            │
            ├── two_link_leg.py
            │
            └── test_two_link_leg.py

File 1 — two_link_leg.py

Contains our actual robotics mathematics:
def forward_kinematics(...):
    ...

def inverse_kinematics(...):
    ...

Its purpose is to calculate robot joint positions and angles.

File 2 — test_two_link_leg.py

Contains our automated tests:

    Forward-kinematics tests
    Inverse-kinematics tests
    Reachability tests
    Joint-limit tests
    Invalid-input tests
    IK → FK verification tests

Its purpose is to check whether our calculations work correctly.

This is called separation of concerns.
Why is this important for Mission Korea?

Imagine that, in 2028, a professor opens your GitHub repository.

A project containing mathematical functions, organized tests, and documented experiments is easier to inspect and evaluate than a single large file containing everything mixed together.

But the benefit isn't just presentation.

Good tests allow us to change our robotics software and check whether we've accidentally broken something.

For example, today we introduced knee-joint limits. Our earlier minimum-reach test revealed that the expected behavior had changed.

That's useful engineering feedback.
3. One important lesson about testing

Not every failing test means your program is wrong.

Sometimes it means:

    Your program contains a bug.
    Your test contains a bug.
    You've intentionally changed the program's requirements, so the old test needs updating.

Today, we encountered the third situation.

Originally, our IK solver allowed a 180° knee angle.

Now we've introduced a maximum of 135°.

Therefore, the old test expecting 180° is no longer appropriate for the updated solver.

We shouldn't blindly delete failing tests. We should understand why they fail and update them when the requirements change.
🎓 Your next checkpoint

For now, keep all your existing tests in two_link_leg.py. We'll move them into a separate test file together in a later session.

Make only this change today:

Replace the old minimum-reach unpacking and angle assertions with:
assert minimum_reach_result is None

Then run your program again.

Does it now execute without a TypeError or AssertionError?

Once it passes, we'll begin organizing your robotics code into proper implementation and testing files.

Keep the updated joint-limit test focused

    Show the cleaned-up test section

radip@aorus-robotics:~/mission-korea/projects/humanoid-robot/kinematics$ python3 two_link_leg.py 
Target reachable.joint angles calculated.
Knee Cordinates: (0.00, -0.40) | Foot Coordinates: (0.40, -0.40)
hip_angle_in_radians: 0.0
knee_angle_in_radians: 1.5707963267948966
Calculated thigh length: 0.4
knee_x: 0.0, knee_z: -0.4
foot_x: 0.4, foot_z: -0.4
straight_line_distance: 0.5656854249492381
straight_foot_x: 0.0, straight_foot_z: -0.8
Unequal leg foot: (0.3, -0.5)
IK verification: (0.30000000000000004, -0.4)
Hip_Angle: 1.954691
knee_angle: 107.457603
Result : (0.034115800762489434, 1.8754889808102941)
Maximum reach result: (0.0, 0.0)
Minimum reach result: None
it passed

Good. ✅ Your updated inverse-kinematics solver passed its tests, including the new knee-joint limit.
🤖 Mission Korea 2028 — Progress Review

Your terminal confirms three important results:
Test	Result	Status
IK → FK verification	Foot reaches (0.3, -0.4) m	✅
Maximum reach	Hip 0°, knee 0°	✅
Minimum reach with 135° knee limit	None	✅

Notice the last result:
Minimum reach result: None

Previously, your solver accepted a 180° knee angle. Now it correctly rejects that solution because our hypothetical knee limit is 135°.

This means your solver is beginning to account for mechanical constraints, not just mathematical geometry.
Today's Next Task — Organizing Our Robotics Code

You've also asked whether you should keep all the function calls and assertions.

My recommendation is yes, keep the tests, but separate them from the mathematical functions.

We'll work towards this structure:
kinematics/
│
├── two_link_leg.py
│   ├── forward_kinematics()
│   └── inverse_kinematics()
│
└── test_two_link_leg.py
    ├── FK tests
    ├── IK tests
    ├── Reachability tests
    ├── Joint-limit tests
    └── Invalid-input tests

This will teach you how Python modules and automated testing work.
Step 1 — Preserve your existing work

Open your terminal:

cd ~/mission-korea/projects/humanoid-robot/kinematics

Create a copy of your current program:

cp two_link_leg.py test_two_link_leg.py

Now you'll have two files containing the same working code.

Don't delete or modify anything yet.

In the next step, we'll separate the two mathematical functions from the experiments and learn how Python imports functions from another file.

That way, you'll preserve all your existing tests while making your project easier to maintain.

Your checkpoint: Create the copy and confirm both files exist using:

ls -l two_link_leg.py test_two_link_leg.py

We'll then continue with the actual code separation.

Keep the working tests organized

    Show the cleaned-up file split

for today i think we should stop here. give me md file from last when we update to until now mentioning what i learn and how and mistakes and what i learn . give me with mkdir -p and nano
Worked for 2m 36s
🤖 Mission Korea 2028 — Learning Log Complete

We've finished today's session. I've created your detailed Markdown notes covering Days 68–70 (18–25 October 2026), continuing from your previous Day 67 learning log.
📘 Download your Markdown file

The file contains:

    Mathematics: FK, IK, reachability, law of cosines, knee and hip angles.
    Programming progress: How you built your reusable inverse_kinematics() function.
    Mistakes and corrections: Syntax errors, function calls, None, and versus or, radians, and debugging.
    Experiments: Successful FK/IK verification, unreachable targets, invalid dimensions, and joint limits.
    Learning evidence: Actual terminal results and completed tests.
    Next session: The exact point where we'll resume.

I also included your own explanations and what you learned from each mistake.
Step 1 — Create the folder

Open your Ubuntu terminal:

cd ~/mission-korea

mkdir -p learning-log/2026/Day-68-to-70-Inverse-Kinematics

Step 2 — Open your Markdown file

nano learning-log/2026/Day-68-to-70-Inverse-Kinematics/day-68-to-70-notes.md

Copy the contents of the downloaded Markdown file into Nano.

Save:

    Ctrl + O → Enter
    Ctrl + X

Step 3 — Save to GitHub

After saving:

cd ~/mission-korea

git add learning-log/2026/Day-68-to-70-Inverse-Kinematics/

git commit -m "docs: complete Days 68-70 inverse kinematics learning log"

git push origin main

📍 Where we'll resume next time

Next topic: Organizing our robotics Python project.

We'll separate:

two_link_leg.py → Mathematical functions.

test_two_link_leg.py → Automated tests.

Your last confirmed experiment was successful, including rejecting the minimum-reach configuration because of the 135° knee limit.

We stopped just before making a backup copy and separating the files.

We'll resume from there without repeating the previous lessons.

Good work today. You're learning not only robotics mathematics but also how to debug, validate, and improve your own software.

Mission Korea 2028 — Today's session complete. 🇰🇷🤖
day-68-to-70-inverse-kinematics-learning-log.mdDocument
Mission Korea 2028 — Humanoid Robotics Learning Log

Study block: Days 68–70 (continued across 18–25 October 2026)
Previous log: Day 67 — Forward-Kinematics Testing & Introduction to IK
Project: Two-link humanoid leg, forward and inverse kinematics
Repository: ~/mission-korea
Code: projects/humanoid-robot/kinematics/two_link_leg.py
Status at stopping point: IK implementation and selected validation tests working; code/test separation planned, not yet confirmed completed.

    Purpose of these notes: Capture what I actually studied, implemented, got wrong, corrected, and learned—so I can resume without repeating the lessons. This log records my work after the Day 67 update.

1. What I set out to learn

I wanted to understand inverse kinematics (IK) properly, not only memorize its equations. I continued from a working two-link forward-kinematics (FK) function and asked why FK and IK matter for humanoid robotics. My immediate programming goal was to develop a reusable IK function for a simplified, planar leg, then check it by feeding its angles back into FK.

Why kinematics matters: FK estimates a robot part's position from known joint angles; IK calculates angles that could place the part at a desired location. For a future humanoid kitchen robot, these tools support planning foot placement and reaching with hands. Kinematics by itself does not handle forces, torque, gravity, balance, collision avoidance, or full-body motion.
Geometry and angle convention (unchanged)

    Work in a 2D X–Z plane. Hip at (0, 0); X forward/right, Z upward; negative Z downward.
    Thigh length L1; shin length L2 (metres).
    Hip angle theta1 = 0 means thigh pointing vertically down.
    Knee angle theta2 is the shin's rotation relative to the thigh; shin world-relative angle is theta1 + theta2.
    The model has ideal zero-thickness links and initially unrestricted joints. Later I added a hypothetical knee limit of 135°.
    Python's math.sin, math.cos, math.atan2 and math.acos operate with/return radians.

2. The central FK and IK formulas
Forward kinematics: angles → position

Given L1, L2, hip theta1 and knee theta2:
xk=L1sin⁡(θ1),zk=−L1cos⁡(θ1)
xk​=L1​sin(θ1​),zk​=−L1​cos(θ1​)
xf=xk+L2sin⁡(θ1+θ2)
xf​=xk​+L2​sin(θ1​+θ2​)
zf=zk−L2cos⁡(θ1+θ2)
zf​=zk​−L2​cos(θ1​+θ2​)

I had already implemented:
def forward_kinematics(thigh_length, shin_length, hip_angle, knee_angle):
    ...
    return knee_x, knee_z, foot_x, foot_z

Four inputs, four outputs. Inputs are on the right of =, inside the function call; calculated values are assigned to the variables on the left. The variable prefix (straight_, unequal_, verified_) is only a useful label; it does not change the calculation.
Target distance and geometric reachability

For target foot position (target_x, target_z) relative to hip (0, 0):
d=xf2+zf2
d=xf2​+zf2​
​
dmin⁡=∣L1−L2∣,dmax⁡=L1+L2
dmin​=∣L1​−L2​∣,dmax​=L1​+L2​
∣L1−L2∣≤d≤L1+L2
∣L1​−L2​∣≤d≤L1​+L2​​

These inequalities test geometric reachability in the ideal model, not whether motors, actual joints, foot contacts, or the rest of the robot can achieve the pose.
Knee angle from the law of cosines
cos⁡(θ2)=d2−L12−L222L1L2
cos(θ2​)=2L1​L2​d2−L12​−L22​​
θ2=±arccos⁡(d2−L12−L222L1L2)
θ2​=±arccos(2L1​L2​d2−L12​−L22​​)

My current IK function takes the positive knee-angle branch from math.acos(). Other geometric solutions may exist.

Critical formula correction I learned: L1**2 and L2**2 occur in the numerator, but the denominator is 2 * L1 * L2—not 2 * L1**2 * L2**2.
Hip angle
α=atan2⁡(xf,−zf)
α=atan2(xf​,−zf​)
γ=atan2⁡(L2sin⁡θ2,  L1+L2cos⁡θ2)
γ=atan2(L2​sinθ2​,L1​+L2​cosθ2​)
θ1=α−γ
θ1​=α−γ​

alpha is the direction from hip to desired foot position. gamma is the angular offset due to the bent leg. I keep angles in radians through the calculation and convert only when printing in degrees.
3. Worked example I solved, then implemented

Robot: L1 = 0.5 m, L2 = 0.3 m
Desired foot: (x, z) = (0.3, -0.4) m

    Distance: sqrt(0.3**2 + (-0.4)**2) = 0.5 m.
    Reach range: 0.2 m <= 0.5 m <= 0.8 m → geometrically reachable.
    Cosine of knee: (0.5**2 - 0.5**2 - 0.3**2) / (2*0.5*0.3) = -0.3.
    Knee: acos(-0.3) = 107.4576031237221° (approximately 1.8754889808102941 radians).
    Target direction: atan2(0.3, 0.4) = 36.86989764584402°.
    Angular difference: atan2(0.3*sin(theta2), 0.5+0.3*cos(theta2)) = 34.91520624744418°.
    Hip: 36.86989764584402° - 34.91520624744418° = 1.954691398399838° (approximately 0.034115800762489434 radians).

My successful IK → FK verification

I used the angles returned by my reusable IK function, not hard-coded manual angles, as inputs to my existing FK function:
ik_hip_angle, ik_knee_angle = inverse_kinematics(0.5, 0.3, 0.3, -0.4)

verified_knee_x, verified_knee_z, verified_foot_x, verified_foot_z = forward_kinematics(
    0.5, 0.3, ik_hip_angle, ik_knee_angle
)

assert math.isclose(verified_foot_x, 0.3, abs_tol=1e-9)
assert math.isclose(verified_foot_z, -0.4, abs_tol=1e-9)

Observed terminal output: IK verification: (0.30000000000000004, -0.4); both round-trip assertions passed.

What I learned: IK solves a target → angles problem; FK solves angles → position. Putting them together creates a round-trip consistency check. 0.30000000000000004 versus 0.3 is negligible floating-point representation error; math.isclose() is appropriate.
4. How I built the reusable inverse_kinematics() function

Signature:
def inverse_kinematics(thigh_length, shin_length, target_x, target_z):

Arguments: link lengths + target coordinates (NOT pre-existing knee/foot coordinates).
Output: (hip_angle, knee_angle) in radians when this branch of IK succeeds; None when rejected.

My implementation evolved through these steps:

    Compute distance from target_x, target_z, rather than reusing foot_x, foot_z from FK.
    Compute minimum reach with abs(thigh_length - shin_length) and maximum reach with thigh_length + shin_length.
    Check is_reachable = distance_minimum <= distance <= distance_maximum.
    if not is_reachable: return None without else: return True.
    Compute a named numerator and denominator, then cos_knee, then knee_angle = math.acos(cos_knee).
    Compute target direction with math.atan2(target_x, -target_z).
    Compute the angular difference with math.atan2(shin_length * math.sin(knee_angle), thigh_length + shin_length * math.cos(knee_angle)).
    Compute hip_angle = target_direction - angular_difference.
    return hip_angle, knee_angle in that exact order.
    Later, add checks for non-positive link lengths and for the hypothetical 135° maximum knee angle.

Current core algorithm (condensed reference, not a replacement for my own file)
def inverse_kinematics(thigh_length, shin_length, target_x, target_z):
    if thigh_length <= 0 or shin_length <= 0:
        return None

    distance = math.sqrt(target_x**2 + target_z**2)
    minimum = abs(thigh_length - shin_length)
    maximum = thigh_length + shin_length
    if not minimum <= distance <= maximum:
        return None

    numerator = distance**2 - thigh_length**2 - shin_length**2
    denominator = 2 * thigh_length * shin_length
    cos_knee = max(-1.0, min(1.0, numerator / denominator))
    knee_angle = math.acos(cos_knee)

    # Hypothetical knee limit in this exercise, not a universal robot specification
    if knee_angle > math.radians(135):
        return None

    target_direction = math.atan2(target_x, -target_z)
    angular_difference = math.atan2(
        shin_length * math.sin(knee_angle),
        thigh_length + shin_length * math.cos(knee_angle),
    )
    hip_angle = target_direction - angular_difference
    return hip_angle, knee_angle

Scope of this implementation: 2D, one knee-bend branch, a maximum knee limit only. It does not validate hip limits, other mechanical collisions, force requirements, or full-body balance. The max/min clamp is meant for very small floating-point excursions after reachability validation, not to magically make unreachable targets possible.
5. Mistakes I made and exactly what they taught me
Mistake / confusion in my work	Correction	What I learned
distance = sqrt(foot_x**2 + foot_z**2) inside IK	Use target_x, target_z	Reusable functions must work from their own arguments, not unrelated variables.
distance_minimum = thigh_length - shin_length	abs(thigh_length - shin_length)	Lengths/distances cannot be negative.
else: return True after unreachable check	Remove early success return; continue computing angles	return ends a function immediately.
numeratir typo/undefined numerator and denominator	Define numerator and denominator correctly	Names must exist and match exactly.
2(thigh_length * shin_length)	2 * (thigh_length * shin_length)	Python multiplication needs *; 2(...) tries to call an integer.
Confused math.atan() with math.atan2() and forgot comma	math.atan2(component_y, component_x)	atan2 takes two distinct arguments; a-b is one subtraction expression.
Used shin_angle from FK in the IK gamma formula	Use IK's knee_angle	Distinguish local IK variables from earlier FK experiments.
Used degree-valued angle inside math.sin()/math.cos()	Keep angle in radians while calculating	Units matter; convert with math.degrees() only to print degrees.
hip_angle = target_distance - angular_distance	target_direction - angular_difference	Similar-looking variable names are not interchangeable; avoid NameError.
Tried knee_x, knee_z, foot_x, foot_z = inverse_kinematics(...)	IK returns two angles, FK returns four coordinates	Function output shape depends on return, not number of inputs.
Tried unpacking None into two angle variables	Store result first; check if result is None	Cannot unpack non-iterable NoneType object; handle failure before unpacking.
Tried return hip_angle, knee_angle = (1.95, 107.46) outside the function	hip_angle, knee_angle = result only after success	Unpacking a result (=) is different from returning from a function (return). Do not hard-code answers.
Wrote else is_reachable:	else:	Python else has no condition.
Wrote if thigh_length <= 0 and shin_length <= 0	Use or	Reject input if either length is invalid, not only when both are invalid.
Old test unpacked expected (hip,knee) at minimum reach after adding knee limit	Update its expected result to None	Test expectations must reflect intentionally changed requirements.
Misleading variable / print label Unreachable result after changing target to reachable	Rename to result / IK result	Variable names are descriptions, not mathematical controls.
Confused where values go in a function call	Inputs inside fn(...); returned values left of =	FK: 4 inputs→4 outputs. IK: 4 inputs→2 outputs or None.
Forgot whether cos_knee/knee_angle should be in else	Prefer simple early-return guard; calculate at 4-space indentation inside function	Python block indentation controls what executes.

Personal learning insight: I often understood the geometry but initially struggled with Python function interfaces, argument order, returned value count, variable names, and the meaning of None. Working through actual errors—not copying a huge finished solution—helped me learn these concepts.
6. Validation tests I actually carried out
A. Reachable IK / FK round-trip — PASSED

    inverse_kinematics(0.5, 0.3, 0.3, -0.4) → approximately (0.034115800762489434, 1.8754889808102941) radians.
    FK with those returned angles gave (0.30000000000000004, -0.4) metres.
    Assertions comparing verified_foot_x with 0.3 and verified_foot_z with -0.4 passed (abs_tol=1e-9).

B. Unreachable target — PASSED

    inverse_kinematics(0.5, 0.3, 1.0, 0.0) → None.
    Maximum reach is 0.8 m; target distance is 1.0 m.
    I learned to avoid unpacking None; first inspect the result with if result is None: ... else: hip_angle, knee_angle = result.

C. Invalid dimensions — PASSED

I wrote and ran tests for invalid inputs, and reported they passed:
assert inverse_kinematics(0.0, 0.3, 0.0, -0.3) is None  # zero thigh
assert inverse_kinematics(0.5, 0.0, 0.0, -0.5) is None  # zero shin
assert inverse_kinematics(-0.5, 0.3, 0.0, -0.3) is None  # negative thigh

I learned to check input validity before evaluating a denominator 2 * L1 * L2; otherwise zero lengths could cause ZeroDivisionError.
D. Maximum reach — PASSED

    inverse_kinematics(0.5, 0.3, 0.0, -0.8) → (0.0, 0.0) radians.
    Fully extended leg; knee angle 0°.
    Distance d=0.8 exactly equals L1+L2 and is allowed in the ideal model.

E. Minimum reach: change in requirements — PASSED after updating test

Before adding mechanical knee limit:

    inverse_kinematics(0.5, 0.3, 0.0, -0.2) → approximately (0.0, pi) radians, corresponding to 180° knee flexion.
    I wrote assertions that hip ≈ 0 and knee ≈ math.pi.

After adding hypothetical knee_angle > math.radians(135) rejection:

    The same call now returns None, because 180° exceeds 135°.
    The earlier unpacking line caused a TypeError until I changed the test expectation.
    The revised test should be:

minimum_reach_result = inverse_kinematics(0.5, 0.3, 0.0, -0.2)
assert minimum_reach_result is None

Observed terminal confirmation: Maximum reach result: (0.0, 0.0) and Minimum reach result: None; final script executed without errors.
7. Important conceptual discoveries
Geometric reachability is not physical feasibility

I explained in my own words that real robot parts have thickness, mass, joints with limited flexibility and mechanical structures; they are not infinitely thin mathematical lines. This was the correct idea. More precise distinction:

    Geometric test: link lengths allow the target in an ideal plane.
    Joint-limit test: the required angles must be within hardware limits.
    Collision checks: solid parts can overlap even when link-line geometry is valid.
    Dynamics: gravity, mass, torque, acceleration and balance require additional modelling/control.

In this exercise a knee allowed only 0° to 135° rejects a 180° IK solution. The 135° limit is an example, not a claim about all humanoid robots.
Boundary and singular-configuration awareness

    Full extension: theta2=0, max reach.
    Full fold: theta2=pi, min reach (if joints permit it).
    These configurations are important in later Jacobian/differential-kinematics lessons; motion control can become ill-conditioned near singularities. We have not implemented Jacobians yet.

Testing is part of robotics engineering

When changing solver requirements, do not simply delete a failing test. Determine whether (a) code is wrong, (b) the test is wrong, or (c) expected behaviour intentionally changed. This time the 180° case shifted from accepted to rejected after adding joint limits.
8. State of my project when I stopped

Working file:
~/mission-korea/projects/humanoid-robot/kinematics/two_link_leg.py

It currently contains both reusable kinematics functions and many experiment calls, print statements, assertions and visualisation code. The most recent reported terminal run showed:
Target reachable.joint angles calculated.
Knee Cordinates: (0.00, -0.40) | Foot Coordinates: (0.40, -0.40)
hip_angle_in_radians: 0.0
knee_angle_in_radians: 1.5707963267948966
Calculated thigh length: 0.4
knee_x: 0.0, knee_z: -0.4
foot_x: 0.4, foot_z: -0.4
straight_line_distance: 0.5656854249492381
straight_foot_x: 0.0, straight_foot_z: -0.8
Unequal leg foot: (0.3, -0.5)
IK verification: (0.30000000000000004, -0.4)
Hip_Angle: 1.954691
knee_angle: 107.457603
Result : (0.034115800762489434, 1.8754889808102941)
Maximum reach result: (0.0, 0.0)
Minimum reach result: None

That successful run is the current confirmed evidence. The earlier suggestions to copy/split the file have not been confirmed done, so I should not claim that a separate test file already exists.
Recommended cleanup (next session; NOT yet completed)

Keep all successful tests as a regression suite, but move them out of the robot-math implementation file. Suggested layout:
kinematics/
├── two_link_leg.py          # forward_kinematics, inverse_kinematics
└── test_two_link_leg.py     # FK, IK, boundary, invalid-input, joint-limit tests

Exact resumption point:

    Back up the known-working script before any refactor:
    cd ~/mission-korea/projects/humanoid-robot/kinematics
    cp two_link_leg.py test_two_link_leg.py
    ls -l two_link_leg.py test_two_link_leg.py

    This cp command was the last proposed checkpoint; I stopped before confirming it was executed. After copying, the files will initially contain duplicate code; we must carefully separate functions from tests next.

    Learn Python import and if __name__ == "__main__": step by step so importing two_link_leg.py for tests does not run all its plots and demo prints.

    Move existing assertions into a dedicated test module, keeping both reachable and rejected cases. Fix the old minimum-reach test to expect None under the 135° limit.

    Run tests after each small change, then commit/push through my usual Git workflow only after verifying.

    Future improvements: distinguish None cases (invalid dimensions, unreachable geometry, joint-limit rejection), handle non-finite values, numerical tolerances near boundaries, alternative knee branches and joint limits for the hip; later study 3D kinematics, Jacobians, dynamics and balance.

Learning style for resumption: Explain the concept → relate to robot → give pseudocode or tiny controlled edit → I write the code → inspect my output. Do not dump a complete refactor.
Learning Evidence

    Primary code evidence: projects/humanoid-robot/kinematics/two_link_leg.py
    Tests demonstrated in terminal: FK configurations, IK/FK round trip, unreachable target, zero/negative link dimensions, max reach and 135° knee-limit rejection.
    Learning evidence link / recording: Add a YouTube link or screenshot/reference only if I actually create one; none supplied for this study block.
    Git commit: Not recorded in this session. Add commit SHA after committing.

My short reflection

I can now explain the difference between FK and IK and implement the main two-link equations in Python. I made repeated mistakes with function calls and returned values but learned how argument positions, multiple return values, and None work. Testing boundaries revealed why mathematical reachability alone is not sufficient for a real robot. My next improvement is to organize and preserve my tests rather than keep growing one script.


