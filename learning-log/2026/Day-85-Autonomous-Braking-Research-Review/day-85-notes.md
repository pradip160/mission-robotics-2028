# Day 85 — Autonomous Braking Research: Catch-up Notes (Days 81–85)

**Mission:** Mission World 2028 — Embodied Robotics  
**Period covered:** 22–27 November 2026  
**Previous confirmed log:** Day 80 — Suspension Dynamics and Autonomous Motion Control (21 November 2026)  
**Current project:** ROS 2 Jazzy + Gazebo restaurant delivery robot  
**Status:** Standalone Python braking experiments completed; ROS 2/Gazebo motion-command integration **not yet verified**.

> **Purpose of this catch-up note:** Reconstruct the work since Day 80 so I can return after a break, understand *why* we made each design choice, and reproduce the next steps. It documents evidence, assumptions, errors, and remaining work rather than claiming the controller is ready for a real robot.

## 1. The research problem

Our restaurant robot transports food, potentially including hot soup. It must stop safely near people and obstacles without unnecessary aggressive braking. Earlier I studied vibration, damping, and how different speeds can affect cargo. The next question was: **how should the robot automatically choose *when* to brake and *how hard* to brake?**

We separated three concerns:

1. **Safety requirement:** avoid collision and preserve an assumed clearance.
2. **Motion policy:** continue, gently brake, or brake hard based on the situation.
3. **Plant response:** the robot may not achieve the deceleration requested by the controller.

The daily objective was practical: derive, implement, test, analyze, and improve a small braking controller rather than only discuss theory.

## 2. Main mathematical model

For forward movement with speed `v >= 0` and constant positive braking magnitude `b > 0`:

```text
braking_distance = v² / (2b)
reaction_distance = v * reaction_time
required_safe_distance = reaction_distance + braking_distance + safety_margin
available_braking_distance = obstacle_distance - reaction_distance - safety_margin
required_braking = v² / (2 * available_braking_distance)  # ONLY if available > 0
next_velocity = max(0, current_velocity - braking * dt)
```

**Units:** velocity = m/s; braking = m/s²; distance = m; time = s. A mistake I corrected was adding `reaction_time` (seconds) to stopping distances (metres), rather than adding `reaction_distance`.

**Numerical integration:** Our first simulator used `displacement = speed * dt`, which overestimates travel while decelerating. We improved it using the constant-acceleration equation and stopping-time clipping:

```python
if deceleration > 0:
    stopping_time = robot_speed / deceleration
    effective_dt = min(dt, stopping_time)
else:
    effective_dt = dt

displacement = (
    robot_speed * effective_dt
    - 0.5 * deceleration * effective_dt**2
)
obstacle_distance -= displacement
robot_speed = max(0.0, robot_speed - deceleration * effective_dt)
```

This works for our simplified straight-line constant-deceleration steps. A complete model must separately represent sensor-to-actuator delay and real response limits.

## 3. Experiments and results

The figures below are from the **reported Python experiments and reviewed mathematical checks**, not hardware tests.

### Experiments A–C: Early fixed-braking simulation

Parameters: `v0 = 0.30 m/s`, `gentle = 0.09 m/s²`, `emergency = 0.50 m/s²`, `reaction_time = 0.10 s`, `safety_margin = 0.10 m`, `early_braking_buffer = 0.10 m`.

| Initial obstacle distance | Reported final clearance with first discrete method | Interpretation |
|---:|---:|---|
| 0.80 m | ~0.195 m | Started by continuing, then gentle braking |
| 0.40 m | ~0.113 m | Emergency, then gentle braking as speed fell |
| 0.15 m | ~0.045 m | Maximum emergency braking; **margin violated** |

I learned that changing decisions as speed decreases can be physically reasonable, but switching too often may produce undesirable acceleration commands.

### Numerical accuracy experiment (0.15 m obstacle)

After correcting displacement integration, `dt = 0.10`, `0.05`, and `0.01 s` all gave approximately **0.0600 m final clearance**, **0.0 m/s final velocity**, and **0.60 s simulated stop time** in the constant-emergency-braking case. This agrees with analytical braking travel `0.30²/(2×0.50) = 0.09 m`; `0.15 - 0.09 = 0.06 m`.

**Do not overgeneralize:** matching the analytic solution here does not validate state decisions, sensor latency, or physical robot dynamics. The reaction time influenced the policy thresholds but was *not actually simulated* as a delayed response.

### Experiment 5/6: Controller with and without state memory

Both approaches started at `0.30 m/s`, `0.80 m`, with `dt = 0.10 s` and improved integration.

| Metric | Controller A: stateless thresholds | Controller B: state memory |
|---|---:|---:|
| Final clearance | 0.2001 m | 0.2100 m |
| Reported simulated duration | 4.00 s | 3.70 s |
| Action transitions | 5 | 1 |
| Returned to `CONTINUE` after braking | Yes | No |
| Minimum 0.10 m clearance | Met in this test | Met in this test |

**Hypothesis supported in this scenario:** state memory reduced repeated switching. This does *not* prove Controller B is universally better: it might stay stopped/braking unnecessarily if an obstacle moves away.

Our tested conservative state-machine policy was:

```python
if previous_action == "EMERGENCY_BRAKE" or obstacle_distance <= gentle_stopping_distance:
    action, deceleration = "EMERGENCY_BRAKE", emergency_braking
elif previous_action == "GENTLE_BRAKE" or obstacle_distance <= gentle_start:
    action, deceleration = "GENTLE_BRAKE", gentle_braking
else:
    action, deceleration = "CONTINUE", 0.0

if action != previous_action:
    transition_count += 1
previous_action = action
```

**Coding mistake:** I initially used `>` instead of `<=` in a threshold condition, misspelled `GENTLE_BRAKE`, and omitted a `CONTINUE` branch. That made gentle braking start immediately at 0.80 m. Manually tracing Boolean expressions and logging each state exposed it. I implemented this state-machine fix **with mentor assistance**, not entirely independently.

### Experiment 7: Conservative emergency braking

At `v0 = 0.30 m/s`, obstacle `0.40 m`, `b = 0.50 m/s²`:

- Simulated final clearance: **0.3100 m**.
- Final speed: **0 m/s** after **0.60 s**; **one transition**.
- Emergency braking travelled `0.09 m` under the immediate-braking model.
- **Trade-off:** hard braking preserves generous distance but may be unnecessarily aggressive for carrying hot soup.

The correct goal is not always maximum braking; it is satisfying safety constraints without unnecessary motion disturbance. A cargo cover or stabilised tray could be worth exploring later, but we have not tested those ideas.

## 4. Adaptive braking: selecting a continuous deceleration

Instead of only `0.09` or `0.50 m/s²`, I wrote `adaptive_braking.py`, which calculates the *minimum modelled braking magnitude needed* to achieve the specified clearance, or selects the maximum if infeasible. This component **assumes a stop has already been requested**; it does not decide when to begin approaching/braking.

My independently written logic:

```text
Calculate reaction distance and available braking distance
IF available distance <= 0:
    command maximum braking; mark infeasible
ELSE:
    required = speed² / (2 * available distance)
    IF required <= maximum braking:
        command required braking; mark feasible
    ELSE:
        command maximum braking; mark infeasible
```

Using `v = 0.30 m/s`, `reaction_time = 0.10 s`, `safety_margin = 0.10 m`, `max_braking = 0.50 m/s²`:

| Obstacle distance | Available braking distance | Required braking | Commanded braking | Margin feasible? |
|---:|---:|---:|---:|---|
| 0.40 m | 0.27 m | ~0.167 m/s² | ~0.167 m/s² | Yes, ideal boundary |
| 0.15 m | 0.02 m | 2.25 m/s² | 0.50 m/s² | No |
| 0.08 m | −0.05 m | Not defined for policy | 0.50 m/s² | No |

I later added predicted physical stopping distance and clearance:

```text
predicted_total_stop = speed * reaction_time + speed² / (2 * commanded_braking)
predicted_clearance = obstacle_distance - predicted_total_stop
```

For example, at 0.15 m: predicted clearance `0.03 m` (**no collision in ideal model, clearance requirement violated**). At 0.10 m: predicted clearance `−0.02 m` (**collision risk**). Negative *available braking distance* does **not** by itself mean the robot already hit the obstacle; it means the desired clearance requirement cannot be met under the model.

### Floating-point boundary lesson

At 0.40 m, predicted clearance was printed as `0.09999999999999998` instead of the mathematical `0.1`, making a naive `>= 0.1` comparison falsely classify a boundary case as `SAFETY_MARGIN_AT_RISK`. Difference: `−2.7755575615628914e−17 m`.

**Learning:** use raw `repr(...)` values to debug; do not round values to force a safety pass. Mark a near-equality as a *numerical boundary case* in tests using a small computation-only tolerance, distinct from physical clearance uncertainty. A real robot needs a deliberate safety allowance, not tolerance-based optimism.

## 5. Research thinking and limitations

**My reasoning:** Sandwiches and hot soup may justify different *normal* motion profiles; the priority remains protecting people and avoiding collisions. Emergency braking can itself spill hot liquid, so cargo stability and collision safety need a joint evaluation. To improve adaptive control, first measure commanded versus achieved acceleration, rather than immediately replacing actuators.

**Example diagnostic (not an actual Gazebo measurement):** commanded `0.167 m/s²` but observed `0.120 m/s²`. The observed magnitude is ~28% smaller. Investigate actual velocity over time, controller update rate, actuator model, wheel/floor friction, load, and sensor feedback through controlled tests. A model prediction is not proof of achieved motion.

**What this work has NOT shown:**

- No validated physical braking safety or hot-soup stability measurement.
- No live ROS 2 velocity command to Gazebo actuators yet in this study segment.
- No verified `/odom` feedback path or closed-loop velocity-tracking experiment yet.
- No realistic reaction-delay simulation, moving obstacles, varying friction, or sensor uncertainty experiment.
- No demonstration that the adaptive controller alone selects an appropriate *braking start time*.

## 6. Skills: demonstrated vs still developing

**Evidence demonstrated:** implemented and ran a basic discrete-time simulator, corrected constant-deceleration integration with guidance, tested a simple state machine, independently wrote the one-step adaptive deceleration decision, compared baselines and experimental outcomes, and debugged floating-point precision.

**Needs more independent practice:** translating mathematics accurately into Python, writing Boolean state transitions without examples, comparing model output against observed motion, experiment design and reproducibility, and ROS 2/Gazebo integration.

## 7. Next session — Day 85 ROS 2 integration checkpoint

The next major milestone is **make the existing Gazebo restaurant robot receive a numerical velocity command and measure its actual motion**. Do not restart the entire robot project or add SLAM yet.

1. Source Jazzy and the existing workspace.
2. Launch the **existing** restaurant robot as normally done.
3. Inspect current nodes and typed topics; determine whether `/cmd_vel`, `/odom`, LiDAR and the existing `/motor_command` are present and connected to Gazebo.
4. Verify whether changing numerical velocity commands moves the simulated robot; if not, identify the smallest missing interface/controller.
5. Measure commanded vs observed velocity before porting the adaptive-braking algorithm.

```bash
source /opt/ros/jazzy/setup.bash
cd ~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws
source install/setup.bash
ros2 node list
ros2 topic list -t
```

**Pause point / next question:** Our old `/motor_command` used symbolic instructions like `MOVE_FORWARD` and `STOP`; adaptive braking needs numerical velocity commands plus feedback. What is already implemented in the current ROS 2/Gazebo system, and what interface is missing?

## 8. How to reproduce this work later

- Files on my Ubuntu machine during study: `~/practice.py` (original/braking-state simulation) and `~/adaptive_braking.py` (one-step adaptive braking). Their exact latest contents must be checked before committing; only code excerpts and terminal output were shared in the study conversation.
- Re-run the experiments with initial speeds, obstacle distances and `dt` values listed above.
- Record initial conditions, controller version, final clearance, elapsed time, state changes and whether the margin was maintained.
- Save code separately under the appropriate project directory *after reviewing it*; this Markdown note is the retrospective learning log, not a claim that code has been committed.

### Takeaway

> I am moving from understanding braking equations to implementing measurable robot behaviour. A simulation that prints `SAFE STOP` is not enough: I must verify units, numerical integration, state transitions, assumptions, and eventually the simulated robot's **observed** velocity. Next: connect our motion supervisor to ROS 2 and Gazebo and compare command against feedback.
