# Mission World 2028 — Daily Robotics Learning Log

**Date:** 2026-11-19  
**Project:** ROS 2 Restaurant Delivery Robot — Robot V2  
**Study focus:** Spring preload, suspension sag, available travel, bottoming out, and food payload stability  
**Session type:** Theory, worked calculations, and engineering reasoning (no SDF or ROS 2 changes)

## Goal

Understand how initial spring preload changes suspension operating position, distinguish spring compression from mechanical travel, and explain why limited compression travel can transmit a disturbance to a robot carrying food.

## 1. Concepts studied

### Spring preload

Preload is the initial spring compression set at the suspension's fully extended position, before the normal operating load is applied. For a linear spring:

\[
F = k(x_p + x)
\]

where:

- \(k\): spring stiffness in N/m;
- \(x_p\): initial preload compression in m;
- \(x\): additional displacement of the suspension from full extension in m.

The preload force is \(F_p=kx_p\). **Preload does not change the stiffness of an ideal linear spring.** It changes the position at which the suspension operates and the force needed to move it away from full extension.

### Distinguishing three measurements

1. **Preload compression:** initial spring compression before static load.
2. **Static sag:** suspension movement from full extension caused by the robot's resting load.
3. **Total spring compression:** preload compression plus the suspension movement from full extension.

Mechanical suspension travel is measured between the full-extension and full-compression stops. Initial spring preload is not additional mechanical travel.

### Why both compression and extension travel matter

- A **bump** requires the wheel to rise relative to the chassis, using compression travel.
- A **depression or pothole** requires the wheel to drop relative to the chassis, using extension travel.
- Excessive preload can reduce static sag and leave less extension travel, potentially allowing a wheel to lose floor contact.
- Preload is not universally specified as 20–30%. A sag percentage may be a useful starting point in some applications, but the appropriate settings depend on suspension geometry, loads, wheel contact and expected floor disturbances.

## 2. Worked exercise: preload and a floor bump

**Assumptions:** linear spring, direct vertical suspension motion, no damping, and chassis momentarily stationary while the wheel travels up over the bump.

| Parameter | Value |
|---|---:|
| Spring stiffness | 10,000 N/m |
| Initial preload compression | 3 mm |
| Static supported load | 90 N |
| Total mechanical travel | 30 mm |
| Bump height | 7 mm |

**Q1 — Preload force**

\[
F_p = 10000(0.003) = \boxed{30\ \mathrm N}
\]

**Q2 — Additional static suspension compression**

\[
x_{\mathrm{sag}}=(90-30)/10000=0.006\ \mathrm m=\boxed{6\ \mathrm{mm}}
\]

**Q3 — Total spring compression at rest**

\[
x_{\mathrm{spring,rest}}=3+6=\boxed{9\ \mathrm{mm}}
\]

**Q4 — Spring force during the simplified bump event**

\[
x_{\mathrm{spring,bump}}=3+6+7=16\ \mathrm{mm}
\]

\[
F_{\mathrm{bump}}=10000(0.016)=\boxed{160\ \mathrm N}
\]

Compared with the 90 N resting spring force, the incremental spring force is 70 N. This is a simplified quasi-static calculation, not a prediction of true impact force.

**Q5 — Remaining compression travel**

\[
x_{\mathrm{travel,used}}=6+7=13\ \mathrm{mm}
\]

\[
x_{\mathrm{remaining}}=30-13=\boxed{17\ \mathrm{mm}}
\]

**Key correction from my exercise:** I initially mixed up additional sag with total spring compression. I must track preload separately from mechanical movement.

## 3. Conceptual exercise: excessive preload

Increasing spring preload on the same linear spring and under the same static load generally:

- decreases additional suspension sag;
- increases available compression travel;
- decreases available extension travel;
- does **not** increase the spring stiffness.

If preload is sufficiently high that its initial force exceeds the normal supported load, the suspension may remain at its full-extension stop (**topped out**). For the delivery robot this can hinder ground following and reduce traction when a drive wheel encounters a depression.

Preload alone cannot establish an intended wheel-load percentage. Actual wheel loads depend on the whole robot's mass distribution, contact geometry, stiffness and suspension adjustment.

## 4. Final exercise: suspension bottoming out

**Scenario:**

| Quantity | Value |
|---|---:|
| Total suspension travel | 30 mm |
| Static sag | 25 mm |
| Compression travel remaining | 5 mm |
| Upcoming bump | 10 mm |

The bump requires 10 mm of relative wheel movement, but the suspension has only 5 mm left before reaching its mechanical stop. In the simplified fixed-chassis picture, **5 mm of required displacement cannot be accommodated by further spring compression**.

The suspension therefore **bottoms out**. The remaining displacement must be accommodated by some combination of tyre deformation, chassis movement and other compliance; it is not correct to interpret 5 mm as an impact force. A hard stop can produce sharp chassis acceleration.

**Robot V2 consequence:** a sudden shock can disturb liquid, spill soup, shift dishes, and spoil food plating even when no collision occurs.

### My conclusion from today's session

> Suspension has to preserve enough compression and extension travel for the restaurant floor. When a bump exceeds available compression travel, the suspension hits its stop and the chassis can experience a sharp disturbance. For a food-delivery robot, this threatens payload stability and presentation.

## 5. Project implications

- Keep **wheel suspension** as a Robot V2 design requirement, not an implemented feature.
- Evaluate both drive-wheel traction and caster ground following under changing payloads.
- Design for adequate compression **and** extension travel rather than maximising either alone.
- When building the model, distinguish actual chassis acceleration from simplified spring-force calculations.
- Eventually evaluate soup/tray disturbance during bumps, braking and turning; suspension cannot by itself prevent liquid sloshing.

## 6. Progress and next session

**Studied:** wheel torque, axle placement, friction and traction, caster geometry, spring stiffness, Hooke's law, static sag, preload, suspension travel and bottoming out.  
**Not yet implemented:** Robot V2 suspended drive-wheel/caster joints, spring-damper model, Gazebo validation, payload testing.

**Next study:** Damping — why springs bounce, how dampers dissipate energy, underdamped vs critically damped vs overdamped response, and what those dynamics mean for carrying food.

**Next engineering question:** How should we choose a damping coefficient so a wheel can absorb a bump without making the restaurant robot and its dishes continue oscillating?
