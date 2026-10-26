# Mission Korea 2028 — Day 71 Learning Notes

**Date:** Monday, 26 October 2026  
**Project:** Humanoid Robot — Two-Link Leg Kinematics  
**Session focus:** Refactoring Python modules, automated testing with pytest, and separate leg visualization

## Today's Objectives

- Separate reusable forward-kinematics (FK) and inverse-kinematics (IK) mathematics from experiments.
- Learn how Python imports functions from another module.
- Convert manual experiments into named automated tests.
- Verify FK and IK with meaningful assertions and run tests using pytest.
- Keep the graphical leg demonstration separate from the test suite.

## 1. Final Project Structure

```text
~/mission-korea/projects/humanoid-robot/kinematics/
├── two_link_leg.py       # Mathematical functions: FK and IK
├── test_two_link_leg.py  # Automated checks using pytest
└── demo_two_link_leg.py  # Matplotlib visual demonstration
```

### Separation of responsibilities

- **`two_link_leg.py`:** Contains `forward_kinematics()` and `inverse_kinematics()`. No test printouts or plotting commands run on import.
- **`test_two_link_leg.py`:** Imports both functions and verifies specified behaviours using `assert` and `math.isclose()`.
- **`demo_two_link_leg.py`:** Imports FK, calculates the hip–knee–foot coordinates, and plots the two-link leg.

**Key principle:** A single mathematical function can be reused by tests, visualizations, and future robot-control code without making duplicate copies.

## 2. Mathematical Model Reviewed

### Coordinate convention

- Hip at `(0, 0)` in the 2D x–z plane.
- Positive x points forward; positive z points upward.
- Hip angle `0` points the thigh straight downward.
- The shin's absolute angle is `hip_angle + knee_angle`.
- Calculations use **radians**. Degrees are useful for displaying angles to humans.

### Forward kinematics

With thigh length `L1`, shin length `L2`, hip angle `θh`, and knee angle `θk`:

```text
knee_x = L1 × sin(θh)
knee_z = −L1 × cos(θh)

foot_x = knee_x + L2 × sin(θh + θk)
foot_z = knee_z − L2 × cos(θh + θk)
```

For `L1 = 0.4 m`, `L2 = 0.4 m`, hip `0°`, and knee `90°`:

- Knee = `(0.0, -0.4)` m
- Foot = `(0.4, -0.4)` m

With both angles at `0°`, the leg is straight and the foot is at `(0.0, -0.8)` m.

### Inverse kinematics and reachability

IK takes a desired foot target `(target_x, target_z)` and attempts to return `(hip_angle, knee_angle)`.

```text
d = √(target_x² + target_z²)
d_min = |L1 − L2|
d_max = L1 + L2
```

- Reject invalid link lengths (`L1 <= 0` or `L2 <= 0`) with `None`.
- Reject targets outside the geometric reach interval with `None`.
- The current solver uses one knee-angle branch and applies a **hypothetical 135° knee limit**; geometrically reachable targets can therefore still be rejected.

For `L1 = 0.5 m`, `L2 = 0.3 m`:

- Maximum geometric reach is `0.8 m`; `(0.0, -0.8)` is reachable with hip and knee angles `(0, 0)` radians.
- `(1.0, 0.0)` is beyond maximum reach and must return `None`.
- `(0.0, -0.2)` is at the geometric minimum-reach boundary but requires a folded knee beyond the configured 135° limit; the present solver returns `None`.

## 3. Python and Testing Skills Learned

### Imported functions

```python
from two_link_leg import forward_kinematics, inverse_kinematics
```

- **Defining** a function does not execute it.
- **Calling** a function executes its body.
- `return` immediately exits a function. It is **not** the same as unpacking a returned tuple:

```python
angles = inverse_kinematics(0.5, 0.3, 0.3, -0.4)
assert angles is not None
hip_angle, knee_angle = angles
```

### Automated tests with pytest

- pytest discovers module-level functions whose names start with `test_`.
- An `assert` that succeeds is normally silent.
- **A test without meaningful assertions can report PASSED without checking the intended result.** We corrected this for the maximum-reach and unreachable-target tests.
- `math.isclose(value, expected, abs_tol=1e-9)` is useful for floating-point coordinate checks.
- Top-level experiment statements execute when pytest imports the file; moving visualization and tests into separate files prevents noisy test collection and plot windows.

### IK → FK round-trip consistency

```text
Desired foot position (0.3, -0.4)
             ↓ IK
        hip and knee angles
             ↓ FK
Calculated foot position ≈ (0.3, -0.4)
```

The test first checks that IK returns a valid result, unpacks the joint angles, passes them into FK, and asserts that the resulting x and z coordinates match the requested foot position.

**Important limitation:** This verifies agreement for the tested target; it is not proof of correctness for every robot pose or every IK branch.

## 4. Automated Tests Completed

| Test | Behaviour checked | Status |
|---|---|---|
| `test_straight_leg` | FK reaches `(0, -0.8)` for a straight 0.4 m + 0.4 m leg | PASS |
| `test_unequal_leg` | FK for 0.5 m thigh, 0.3 m shin, and a 90° knee | PASS |
| `test_invalid_link_lengths` | IK rejects zero or negative segment lengths | PASS |
| `test_maximum_reach` | IK accepts `(0, -0.8)` with lengths 0.5 m + 0.3 m | PASS |
| `test_minimum_reach` | IK rejects `(0, -0.2)` under the 135° knee restriction | PASS |
| `test_unreachable_target` | IK rejects target `(1.0, 0.0)` beyond 0.8 m reach | PASS |
| `test_ik_fk_consistency` | FK reproduces `(0.3, -0.4)` using angles computed by IK | PASS |
| `test_link_lengths` | FK preserves thigh and shin geometric lengths | PASS |

**Verification command:**

```bash
cd ~/mission-korea/projects/humanoid-robot/kinematics
python3 -m pytest test_two_link_leg.py -v
```

**Actual result reported today:**

```text
collected 8 items
...
8 passed in 0.02s
```

## 5. Visualization Evidence

**Command:**

```bash
python3 demo_two_link_leg.py
```

The demonstration successfully displayed the two-link leg by joining the hip, knee, and foot points:

```python
x_positions = [x_hip, knee_x, foot_x]
z_positions = [z_hip, knee_z, foot_z]
plt.plot(x_positions, z_positions, marker="o")
plt.axis("equal")
plt.show()
```

The graph was visually checked and confirmed to display correctly.

## 6. Problems Encountered and Fixed

1. **Function argument typo:** Added a missing comma in a four-argument FK call.
2. **Incorrect use of `return`:** Replaced an early `return hip_angle, knee_angle` inside a test with tuple unpacking so FK and assertions could execute.
3. **Misleading test name:** Renamed a test that checked invalid link lengths; created a separate test for geometrically unreachable foot targets.
4. **False confidence from empty tests:** Added assertions after realising a test can pass without checking its output.
5. **Incorrect maximum-reach expectation:** Recognised a maximum-reach target is reachable and IK correctly returned `(0.0, 0.0)` rather than `None`.
6. **Use of old values:** Updated IK–FK consistency to use IK-calculated angles and freshly computed FK foot coordinates instead of hard-coded or previous experiment values.
7. **Plotting from tests:** Moved Matplotlib visualization into its own demonstration file so pytest runs cleanly and quickly.

## 7. Learning Evidence

- [x] `two_link_leg.py` contains reusable FK and IK functions.
- [x] `test_two_link_leg.py` imports both mathematical functions.
- [x] Eight named pytest functions were discovered and passed.
- [x] `demo_two_link_leg.py` ran and displayed the robot leg correctly.
- [x] Terminal evidence: `8 passed in 0.02s`.
- [ ] YouTube demonstration link: not provided for this day.
- [ ] Git commit or remote push: not confirmed during this session.

## 8. Remaining Cleanup and Next Session

**Small optional cleanup to finish before new material:**

- Move the remaining `x_hip`, `z_hip`, `thigh_length`, and `shin_length` variables inside `test_link_lengths()` so the test is self-contained.
- Remove any remaining unused module-level angle variables from the test file.
- Rerun all eight tests and verify they still pass.

**Next robotics lesson:** The two-link leg **Jacobian**, which connects joint angular velocities to foot velocity:

```text
Joint velocities (hip_rate, knee_rate)
                  ↓ Jacobian
             Foot velocity (vx, vz)
```

Later topics: Jacobian derivation, velocity kinematics, singularities, and eventually the relationship between forces and joint torques.

## Reflection

Today was primarily a **research software engineering** session. The main achievement was not a new formula; it was converting existing two-link leg mathematics into a clearer, reusable project with reproducible automated tests and a separate visualization. The next session can return to robotics mathematics without losing today's work.
