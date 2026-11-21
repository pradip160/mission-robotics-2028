# Day 80 — Robot V2 Suspension Dynamics, Resonance & Autonomous Speed Control

**Date:** 2026-11-21  
**Project:** Mission World 2028 → ROS 2 Restaurant Delivery Robot → Robot V2  
**Status:** Study complete for today; conceptual design only (not yet implemented in Gazebo).  
**Previous study:** Day 78 — Robot V2 drivetrain/casters/suspension; Day 79 — suspension preload and bottoming out.  
**Next study:** Feedback control when slowing down makes vibration worse → vibration isolation → suspension design/experiments.

> **If I return after a long break, read Sections 1, 5, 8 and 10 first.**  
> **Central question:** How can a standing delivery robot carry soup safely across an imperfect floor *without a human adjusting its speed each time*?

---

## 1. Five-minute recall — what did I actually learn?

1. A **spring** resists displacement and stores energy: `F_s = k x` (magnitude). A **damper** resists relative velocity and dissipates energy: `F_d = -c x_dot` (signed force).
2. With a spring but no damper, the chassis can keep bouncing after a bump. With damping, oscillation energy dissipates. **More damping is not always better**: too much damping can resist wheel movement and transmit sharp disturbances to the body.
3. The damping *classification* depends on **mass, spring stiffness and damping together**, not `c` alone: `zeta = c / (2 sqrt(m k))`.
4. Natural frequency of an ideal one-degree-of-freedom system is `f_n = (1 / (2 pi)) sqrt(k / m)`; **heavier → lower frequency**, **stiffer → higher frequency**.
5. Regularly spaced floor joints create an approximate encounter frequency `f_exc = v / d`. If it approaches the suspension's natural frequency, **resonance may amplify vibration**, depending on damping and disturbance shape.
6. Our robot needs **automatic decisions**, not manually chosen speeds at every obstacle. A proposed *vibration speed supervisor* would use estimated vibration and safety limits to influence a local motion controller.
7. **The next unresolved question:** What if reducing speed from 0.40 to 0.20 m/s makes vibration *worse*? A safe controller needs feedback, limits, alternatives and a stop/fallback strategy—not a rule that always slows down.

### Core physical picture

```text
Restaurant floor bump or joint
        ↓
Wheel / caster moves vertically
        ↓
Spring compresses (stores energy) + damper moves (dissipates energy)
        ↓
Robot chassis acceleration / pitch / roll
        ↓
Tray moves → soup sloshes or plated food is disturbed
        ↓
IMU + state estimation measure what actually happened
        ↓
Controller adjusts *future* motion within safety limits
```

**Do not confuse:** moving the wheel smoothly, quickly settling the chassis, maintaining wheel traction and keeping soup steady are related goals, but not identical metrics.

---

## 2. Prerequisites from Day 78–79 (brief refresher)

### Robot V2 design direction

- Standing restaurant delivery robot with trays; future robot arm is only a longer-term concept, **not part of this stage**.
- Preserve working Robot V1; build Robot V2 separately.
- Candidate layout: two driven wheels plus front/rear casters, with suspension considered at wheel assemblies. The design is preliminary, not validated.
- Uneven floor, load changes, body tilt and soup transport justify studying suspension, damping and gentle acceleration/jerk.

### Spring, preload and travel

- Spring stiffness: `F = k x` with consistent units (`x` in **metres**).
- Static sag is the displacement due to supported load; preload can change where the suspension sits within its available travel, but **does not change linear spring stiffness**.
- Example: 30 mm total suspension travel and 25 mm static sag leaves only 5 mm compression travel. A 10 mm bump could cause **bottoming out** under the simplifying assumptions of our earlier case study.
- A damper is not a replacement for sufficient spring travel or correctly chosen stiffness.

---

## 3. Damping: physical meaning and my answered exercises

### Equations

For an ideal linear spring:

`F_s = -k x`  (restoring-force direction; magnitude `k |x|`)

For an ideal viscous damper:

`F_d = -c x_dot`  (opposes relative velocity; magnitude `c |x_dot|`)

| Symbol | Meaning | Unit |
|---|---|---|
| `x` | Relative compression/displacement | m |
| `x_dot` | Relative suspension velocity | m/s |
| `k` | Linear spring stiffness | N/m |
| `c` | Viscous damping coefficient | N·s/m |

**My calculation (all correct):** `k = 8000 N/m`, `x = 15 mm = 0.015 m`, `c = 300 N·s/m`, `x_dot = 0.20 m/s`.

- Spring-force magnitude: `8000 × 0.015 = 120 N`.
- Damper-force magnitude: `300 × 0.20 = 60 N`.
- If movement stops but the spring remains compressed 15 mm: **damper force = 0 N**, **spring force = 120 N**.
- If the damper is removed, the spring can cause repeated bouncing because stored energy transfers back and forth between spring and mass.

**My misconception, now corrected:** I said overdamping causes unwanted oscillation. **Incorrect.** In the ideal system, **underdamping** oscillates; critical and overdamping are non-oscillatory for the standard displacement-release response. Overdamping is undesirable mainly because it can respond slowly and can transmit large forces during rapid wheel motion, **not** because it produces the characteristic underdamped oscillation.

---

## 4. Damping ratio: how to classify the system

For an ideal vertical **single-degree-of-freedom** mass–spring–damper, measured relative to static equilibrium:

`m x_ddot + c x_dot + k x = 0`  (free vibration)

`c_critical = 2 sqrt(m k)`

`zeta = c / c_critical = c / (2 sqrt(m k))`

| Damping ratio `zeta` | Response classification |
|---|---|
| `< 1` | Underdamped (oscillatory decay) |
| `= 1` | Critically damped |
| `> 1` | Overdamped (non-oscillatory but slower decay) |

### My exercise — `m = 10 kg`, `k = 5000 N/m`, `c = 300 N·s/m`

```text
c_critical = 2 × sqrt(10 × 5000)
           = 447.214 N·s/m
zeta       = 300 / 447.214
           ≈ 0.671 → UNDERDAMPED
```

**My answers:** I wrote `446.2146 N·s/m` for critical damping (small arithmetic error); `0.671` and **underdamped** were correct.

**What if effective suspended mass rises to 20 kg?**

```text
c_critical = 2 × sqrt(20 × 5000) ≈ 632.456 N·s/m
zeta       = 300 / 632.456 ≈ 0.474
```

**Key conclusion I understood:** Higher effective mass with the same `k` and `c` → **lower damping ratio**, even though the coefficient `c` has not changed. This does not automatically prove food sloshes more; test the actual response.

### Is `zeta = 1` always best?

My initial choice was **critical damping** because I want soup to settle without repetitive bouncing. This is a **reasonable initial candidate, not the proven optimum**. A one-time displacement-release test rewards fast settling; a rough floor adds repeated input. Too much damping can increase transmitted forces. Future test candidates: `zeta = 0.4`, `0.7`, `1.0` with the same bump profiles and payloads.

---

## 5. Natural frequency: mass and stiffness change how fast the robot vibrates

For the ideal **undamped** single-degree-of-freedom model:

`f_n = (1 / (2 pi)) sqrt(k / m)` in **Hz**.

- More mass (`m ↑`) → `f_n ↓`.
- Stiffer spring (`k ↑`) → `f_n ↑`.
- **Both light and heavy masses can vibrate naturally.** Lighter does not mean automatically larger oscillation amplitude.
- Frequency is oscillations per second, **not** vibration severity by itself.

### Worked values

| Effective mass | Spring stiffness | Natural frequency |
|---:|---:|---:|
| 10 kg | 5,000 N/m | `3.56 Hz` |
| 20 kg | 5,000 N/m | `2.52 Hz` |
| 10 kg | 10,000 N/m | `5.03 Hz` |

**My answers:**
- Doubling mass makes natural frequency **decrease** — correct.
- Doubling stiffness from 5,000 to 10,000 N/m (with `m = 10 kg`) gives **5.03 Hz** — correct.
- Very stiff springs do **not** automatically protect food. They can transmit stronger, sharper forces under comparable imposed displacements. The complete response depends on damping, floor shape, wheel motion and speed.

**Remember the square roots:** Doubling stiffness increases frequency by `sqrt(2)` (~41%); doubling mass decreases it by `1 / sqrt(2)` (~29%).

---

## 6. Resonance: why one travelling speed can be worse than another

For **regularly spaced** floor joints:

`f_excitation = v / d`  where `v` is travel speed (m/s) and `d` is joint spacing (m).

With `f_n ≈ 5.03 Hz` and `d = 0.10 m`:

| Robot speed | Encounter frequency | Distance from 5.03 Hz |
|---:|---:|---:|
| 0.20 m/s | 2 Hz | 3.03 Hz |
| 0.30 m/s | 3 Hz | 2.03 Hz |
| 0.40 m/s | 4 Hz | 1.03 Hz |
| 0.50 m/s | 5 Hz | 0.03 Hz |
| **0.503 m/s** | **5.03 Hz** | **0 Hz** |
| 0.70 m/s | 7 Hz | 1.97 Hz |

**My exercise:**
- At 0.30 m/s, I found **3 Hz** — correct.
- I incorrectly said 3 Hz was *closer* to resonance than 5 Hz. Actually **5 Hz is far closer** to 5.03 Hz.
- I calculated resonance-speed estimate `v = f_n d = 5.03 × 0.10 = 0.503 m/s` — correct.
- I said increasing speed always makes vibration worse. **Correction:** Increasing speed changes excitation frequency. Moving away from resonance can reduce resonant amplification, but faster wheel impacts may be harsher. **Neither "always speed up" nor "always slow down" is a reliable rule.**

**Unanswered end-of-day comparison:** At 0.40 m/s excitation is 4 Hz (1.03 Hz from natural); at 0.70 m/s it is 7 Hz (1.97 Hz away). So **0.40 m/s is closer to resonance**. But 0.70 m/s is **not guaranteed** to be safer for soup because impact severity, damping, floor profile, wheel-ground contact, body pitch/roll and liquid sloshing matter too.

**Model limitations:** The joints are a sequence of impacts, not a pure sine wave; they can excite multiple frequencies. Our formulas provide intuition, not an automatic final robot speed. Actual four-wheel Robot V2 has multiple modes (bounce, pitch and roll), not one isolated spring-mass mode.

---

## 7. Autonomous decisions: algorithms, controllers and embodied AI

### The question I asked

> We cannot personally adjust the robot each time it finds a bump or obstacle. What *actually* decides—an algorithm, a system or embodied AI?

**Answer:** A practical robot has **several cooperating decision-making components**. Not every action requires AI.

```text
Task planner            "Deliver to Table 7"
      ↓
Global planner          "Which route?"
      ↓
Local motion controller "What velocity/turn should I command?"
      ↑          │
      │          ├── permitted speed/acceleration from a safety or speed supervisor
      │          ↓
      │      Wheel controller → motors → robot moves
      │                                   │
      └──────────── sensors + state estimation + feedback
                          (IMU, odometry, LiDAR, etc.)
```

**Proposed future ROS 2 component:** `vibration_speed_supervisor` (concept only).

Potential responsibilities:

1. Read IMU/chassis-motion information and motion state.
2. Estimate vibration level over time (avoid reacting to a single noisy reading).
3. Combine vibration evidence with payload and safety limits.
4. Restrict commanded **speed, acceleration and jerk** when justified.
5. Reassess the vibration after changing motion—**closed-loop feedback**.
6. If unsafe vibration persists, **stop safely or plan an alternative route**.

```python
# PSEUDOCODE ONLY — NOT IMPLEMENTED
if measurements_unreliable:
    safe_stop()
elif immediate_safety_limit_exceeded:
    safe_stop()
else:
    vibration = estimate_vibration_over_time(imu, robot_state)
    speed_limit = choose_safe_speed_limit(vibration, payload, route_context)
    apply_speed_limit(speed_limit)
    monitor_effect_of_change()
```

**Important sensor distinction:** The IMU can detect vibrations as they happen, subject to gravity compensation, calibration and filtering. A typical horizontal 2D LiDAR **cannot reliably foresee tiny changes in floor height**. Anticipation might need a suitable ground-facing sensor, a known terrain map or previously recorded vibration hotspots.

### Traditional control vs AI

- **Rules/thresholds:** Explicit decisions; simplest starting baseline.
- **PID:** Feedback-based regulation of a quantity.
- **Model Predictive Control:** Predictive optimisation with a model and constraints.
- **Machine learning / reinforcement learning:** Potential later methods for adapting speed decisions from data or interaction.
- **Embodied AI** is the larger goal of perception, decision and action in a physical environment; we should not call every ordinary control rule "AI".

### What currently exists vs what is still proposed

**Already explored/built in the project:** ROS 2 obstacle/status logic, navigation decision node and motor command subscriber that can send velocity commands; Gazebo movement and sensor studies.

**Not yet built/validated:** A vibration-based speed supervisor, complete food-safe motion planner, a tested suspended Robot V2, experimentally verified soup-spill prevention, or a fully integrated Nav2 stack.

Nav2 can be a future navigation foundation; our distinctive research contribution could be **payload- and vibration-aware motion control**, built first with an interpretable baseline and later compared to adaptive/learning methods.

---

## 8. Mistakes I must not repeat

| Mistake / shortcut | Correct understanding |
|---|---|
| "Overdamping creates oscillation." | **Underdamped** response oscillates; overdamped does not in the ideal free-response model. |
| "Higher damping means better food transport." | Trade-off: settling vs transmitting sharp disturbances; **measure**. |
| "A damper has force even when the suspension is stationary." | Ideal viscous damper force is **zero** at zero relative velocity. |
| "Heavier means higher natural frequency." | Same stiffness → **heavier means lower** natural frequency. |
| "Stiffer springs always reduce vibration." | They raise natural frequency and can transmit sharper forces. |
| "Slower always means less vibration." | Slowing down can move excitation **toward** resonance, though many situations still benefit from reduced speed. |
| "Higher speed is always safer once beyond resonance." | Harsher impacts and other dynamic effects can outweigh detuning benefits. |
| "AI directly runs every motor decision." | Robots use **layers of planners, feedback controllers, safety limits and possibly AI**. |
| "We already implemented vibration control." | **No**—we studied and proposed it; implementation comes later. |

---

## 9. Active recall — test myself *before* reading the answer key

If revisiting after several weeks, cover the answer key and try these in a notebook:

1. What does a spring do? What does a damper do? How do their force laws differ?
2. With `k = 8000 N/m`, `x = 0.015 m`, `c = 300 N·s/m`, `v_rel = 0.2 m/s`, find spring and damper force magnitudes.
3. What happens to ideal viscous damping force if relative velocity becomes zero while spring compression remains unchanged?
4. State `c_critical`, `zeta` and the meanings of `zeta < 1`, `= 1`, `> 1`.
5. With `m = 10 kg`, `k = 5000 N/m`, `c = 300 N·s/m`, calculate critical damping and damping ratio.
6. What happens to damping ratio and natural frequency when **effective mass doubles** but `k` and `c` stay fixed?
7. What happens to natural frequency when spring stiffness doubles at the same mass?
8. A robot at 0.5 m/s crosses joints every 0.1 m. What is the excitation frequency? Compare it to 5.03 Hz.
9. Why might reducing speed from 0.4 to 0.2 m/s unexpectedly make vibration worse?
10. Which component would be responsible for changing the permitted speed automatically? Which component actually follows the path?
11. Can a horizontal 2D LiDAR reliably predict every small bump? Which sensor could detect vertical vibration?
12. What must we measure before asserting that one damping choice better protects soup?

<details>
<summary><strong>Answer key — open only after attempting</strong></summary>

1. Spring stores energy / displacement response `F ≈ k x`; damper dissipates energy / velocity response `|F| = c |v_rel|`.
2. `120 N` spring; `60 N` damper.
3. `0 N` ideal damping force; spring still exerts `120 N`.
4. `2 sqrt(mk)`, `c/(2sqrt(mk))`; under / critical / over damping.
5. `447.214 N·s/m`; `0.671` → underdamped.
6. Both `zeta` and `f_n` decrease (assuming a comparable one-DOF system).
7. Multiplies by `sqrt(2)`; e.g. `3.56 Hz` → `5.03 Hz` for `10 kg` and `5000→10000 N/m`.
8. `5 Hz`, very close to `5.03 Hz`.
9. Different speeds change disturbance frequency; speed reduction could move the system closer to another resonance (or affect other dynamics). Measure instead of guessing.
10. Proposed speed/safety supervisor sets limits; local motion controller commands motion along path; lower-level wheel controller executes.
11. No; IMU measures body motion (with correct processing), and other terrain-sensing approaches may predict surface geometry.
12. Chassis/tray accelerations, body tilt, oscillation/settling time, payload stability or slosh, and wheel contact; test across payloads, bumps and speeds.

</details>

---

## 10. START HERE NEXT SESSION — precise continuation checkpoint

### Unresolved engineering scenario

Our Robot V2 carries soup and moves at **0.40 m/s**. The vibration supervisor detects high chassis vibration and limits speed to **0.20 m/s**. **After slowing down, measured vibration is even stronger.**

**My next task:** Propose what an *autonomous feedback controller* should do next. Don't simply assume speeding up is safe or keep reducing speed blindly.

Questions to think through:

- How do we verify that the increase is real (not transient noise, sensor error or delayed effects)?
- Should we stay at 0.20 m/s, try another **safe permitted** speed, stop, or replan?
- Which safety limits (peak acceleration, tilt, clearance, traction and braking distance) must *never* be violated?
- What state/decision logic prevents rapid oscillation between two speeds?
- How would we experimentally compare a simple rule-based speed controller against an adaptive one?

### Planned sequence

1. **Feedback and safety logic:** detection → controlled response → verification → fallback.
2. **Vibration isolation:** understand body-vs-ground response and why settling time is not enough.
3. **Model our Robot V2:** mass distribution, spring stiffness, damping, travel, payload range, and bounce/pitch/roll.
4. **Simulation experiments (later):** repeatable floor disturbances, logged IMU / tray response, speed sweeps, different payloads; compare controllers.
5. Only **after understanding/testing the physics**, consider implementing ROS 2 nodes and Gazebo suspension mechanics.

### What to tell ChatGPT to resume

> Continue Mission World 2028 **after Day 80**. We finished springs, preload, damping coefficient, damping ratio, natural frequency, resonance, and the proposed vibration-aware speed supervisor. Start with the unresolved case: Robot V2 slows from 0.40 to 0.20 m/s, but vibration becomes worse. Teach concept → robot case study → mathematics only where needed → let me answer independently. Do **not** jump into writing code yet.

---

## 11. Learning reflection

**What I did well:**
- Correctly calculated spring force **120 N**, damping force **60 N**, damping ratio **0.671**, natural frequency **5.03 Hz**, and resonance speed **0.503 m/s**.
- Recognised the mass–frequency relationship physically, not just mathematically.
- Asked an architecture question: **Who decides robot speed autonomously?** This connected suspension physics to the full robotics system.

**What I corrected:**
- Overdamping is not the same as oscillation.
- Excitation at 3 Hz is farther from 5.03 Hz than excitation at 5 Hz.
- More speed, less speed, more stiffness or more damping **cannot automatically** be called safer without measuring the system.

**My guiding principle:**

> **Understand the mechanism → calculate → form a prediction → simulate and measure → revise the design.**

*End of Day 80. No new ROS 2 code or Gazebo model changes were made during this study session.*
