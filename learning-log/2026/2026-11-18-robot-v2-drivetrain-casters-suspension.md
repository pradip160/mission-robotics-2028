# Robot V2 — Drivetrain, Caster Mechanics and Suspension

**Project:** Mission World 2028 — Autonomous Restaurant Service Robot  
**Study period:** 12–18 November 2026  
**Environment:** ROS 2 Jazzy, Gazebo Harmonic, SDFormat  
**Status:** Mechanical design study and analytical calculations; V2 implementation and validation pending.

## 1. Objective and design direction

The original restaurant robot is a working learning prototype. Rather than extending its two-drive-wheel, single-caster layout, I plan to develop a separate standing service robot that can carry food and drinks and eventually use a robotic arm to load and unload dishes.

The new platform must balance manoeuvrability, traction, stability and payload protection. I will preserve Robot V1 and develop V2 in a separate SDF file. New components will be studied before implementation.

### Preliminary V2 specification

| Parameter | Candidate value |
| --- | --- |
| External footprint | 0.70 m × 0.65 m |
| Chassis body | 0.70 m × 0.54 m × 0.20 m |
| Standing height | Approximately 1.20–1.25 m |
| Drive layout | Two independently powered central wheels |
| Supporting wheels | Front and rear swivel casters |
| Drive wheel radius / thickness | 0.10 m / 0.05 m |
| Drive wheel centre separation | 0.60 m |
| Caster wheel radius / thickness | 0.05 m / 0.03 m |
| Caster offset | 0.02 m |
| Nominal caster pivot X positions | +0.25 m and −0.25 m |
| Suspension | Spring-damper assemblies under consideration |
| Future payload | Food, drinks and a robotic arm |

These are preliminary design targets, not validated hardware specifications.

## 2. Footprint and turning clearance

I reviewed the restaurant world geometry to identify narrow service passages. Some relevant static clearances are 2.00 m at the kitchen entrance, 1.60 m at the porter entrances, 1.125 m between the porter and staff rooms, and 1.025 m between the kitchen partition and staff room. These measurements do not prove end-to-end route feasibility.

For passage width `P`, external robot width `W` and required per-side clearance `C`:

```math
C_{actual}=\frac{P-W}{2},\qquad W_{max}=P-2C
```

For a conservative rectangular footprint of length `L`, rotating around its centre:

```math
D_{required}=\sqrt{L^2+W^2}+2C
```

Using a 1.20 m corridor and provisional 0.10 m clearance on each side:

| Footprint | Straight clearance per side | Required turning diameter |
| --- | ---: | ---: |
| V1 bounding rectangle: 0.80 × 0.65 m | 0.275 m | 1.231 m |
| V2 candidate: 0.70 × 0.65 m | 0.275 m | 1.155 m |

V2 can theoretically rotate within this corridor with approximately 22.4 mm of additional clearance per side. This assumes ideal in-place rotation and static obstacles. The real footprint and turning trajectory must be tested.

A drive axle shifted 0.10 m forward or backward increases the conservative required turning diameter to approximately 1.310 m. This is why a central drive axle is preferred: it minimises the maximum swept radius for a symmetric rectangular body.

## 3. Drive wheel geometry and torque

The proposed V2 frame origin is at nominal floor level below the drive axle midpoint. X is forward, Y is left, Z is upward.

| Component | Nominal centre (X, Y, Z), m |
| --- | --- |
| Chassis | (0, 0, 0.21) |
| Left drive wheel | (0, 0.30, 0.10) |
| Right drive wheel | (0, −0.30, 0.10) |

The chassis bottom is 0.11 m above the nominal floor. The wheel inner face is at |Y| = 0.275 m, leaving only 5 mm of nominal clearance from the chassis side. This packaging needs review for brackets, suspension movement and tolerances.

The two wheels have independent motors or actuators, not one rigid rotating shaft. The motors are fixed to their mounting assemblies and torque is transmitted through the wheel shafts.

### Key relationships

```math
v=r\omega,\qquad \tau=Fr,\qquad P=\tau\omega=Fv
```

The simple force-to-torque relation neglects wheel rotational acceleration and losses. A more complete wheel equation is:

```math
\tau_{axle}=F_{wheel}r+I\alpha
```

For a uniform 1 kg cylindrical wheel with radius 0.10 m and thickness 0.05 m, oriented along Y:

- `Iyy = 0.005 kg·m²`
- `Ixx = Izz = 0.00270833 kg·m²`

At 0.5 m/s the wheel needs 5 rad/s, approximately 47.75 RPM, with ideal rolling.

A larger wheel increases speed at the same angular velocity but requires more torque for the same traction force. A gearbox trades speed for torque; the output torque depends on gear ratio and efficiency. Real motor selection requires continuous and peak torque, speed, thermal ratings and drivetrain losses.

### Worked torque exercise

Assumptions: 30 kg robot, 0.40 m/s² acceleration, rolling resistance coefficient 0.02, level floor, two driven wheels, wheel radius 0.10 m.

- Acceleration force: `30 × 0.40 = 12 N`
- Rolling resistance: `0.02 × 30 × 9.81 = 5.886 N`
- Total required traction: `17.886 N`
- Torque per wheel: `17.886 / 2 × 0.10 = 0.8943 Nm`
- With a 0.15 m wheel radius: `17.886 / 2 × 0.15 = 1.34145 Nm`

My initial force and torque calculations were correct. I corrected the traction calculation and the larger-radius torque calculation. Increasing radius by 50% increases the required axle torque by 50% if the required force is unchanged.

## 4. Friction, traction and wheel slip

Static friction provides grip during ideal rolling without slipping. Its maximum value is `μs N`; actual static friction depends on the required force. Rolling resistance is a separate loss mechanism and is approximated here by `Crr mg`.

For a 30 kg robot with an assumed 60% of its weight on its driven wheels:

```math
N_{drive}=0.60mg=176.58\ \mathrm{N}
```

The simplified motor and traction limits are:

```math
F_{motor}=\frac{\tau_L+\tau_R}{r},\qquad F_{traction,max}=\mu_s N_{drive}
```

```math
a_{max}=\frac{\min(F_{motor,max},F_{traction,max})-F_{rr}}{m}
```

Assume 1.5 Nm per motor, 0.10 m wheel radius, equal wheel loading and 5.886 N rolling resistance. Neglect rotational inertia and changes in normal force.

| Quantity | Wet floor (μ = 0.15) | Very slippery floor (μ = 0.05) |
| --- | ---: | ---: |
| Ideal motor force | 30 N | 30 N |
| Maximum available traction | 26.487 N | 8.829 N |
| Net force at traction limit | 20.601 N | 2.943 N |
| Maximum non-slip acceleration | 0.6867 m/s² | 0.0981 m/s² |
| Maximum traction-limited axle torque per wheel | 1.32435 Nm | 0.44145 Nm |

At μ = 0.02, the traction limit is only 3.5316 N, smaller than the assumed rolling resistance. Increasing motor torque does not solve the traction-limited problem. Improving wheel grip, drive-wheel loading or rolling efficiency may help.

For this model, the minimum coefficient for sustained forward rolling on level ground is `Crr / 0.60 = 0.0333`. These are illustrative coefficients, not measured restaurant floor properties.

### Connection to odometry

A wheel encoder can measure wheel rotation correctly while the no-slip kinematic model estimates incorrect movement. For forward driving, a simple slip convention is:

```math
s=\frac{r\omega-v_{actual}}{r\omega}
```

With `rω = 0.50 m/s` and actual speed `0.30 m/s`, slip is 40%. After 10 seconds, wheel odometry would estimate 5 m while actual travel would be 3 m, giving a 2 m error. Unequal slip between the two drive wheels can also introduce heading error. This motivates later sensor fusion and localization experiments.

## 5. Caster mechanics and support geometry

A swivel caster consists of a mounting plate, swivel bearing, fork, wheel axle and wheel. It has two passive rotational degrees of freedom:

- Swivel: rotation about the vertical Z axis.
- Rolling: rotation about the local horizontal wheel axle.

Caster offset (trail) is the horizontal separation between the swivel axis and wheel centre. A lateral contact force can produce a self-aligning moment around the swivel axis:

```math
\tau_z=eF_\perp
```

For 20 mm offset and 5 N perpendicular force, the swivel moment is 0.10 Nm. Vertical load at that offset produces a bending moment about a horizontal axis, not a self-aligning moment about Z.

The caster follows the direction of local motion. During reversal it can swivel approximately 180°, temporarily increasing resistance. During in-place rotation the front and rear caster pivots travel in opposite lateral directions.

### Caster packaging

For radius 0.05 m, offset 0.02 m and thickness 0.03 m, the conservative wheel-only swept radius is:

```math
R=\sqrt{(0.02+0.05)^2+0.015^2}\approx0.0716\ \mathrm{m}
```

With a front pivot at X = 0.25 m, the envelope reaches X = 0.3216 m, leaving approximately 28.4 mm before the chassis end at X = 0.35 m. Fork and bearing dimensions are not included.

The caster axle height is nominally 0.05 m; the wheel top is at 0.10 m. This leaves only 10 mm below the chassis before accounting for the fork and suspension, so recessed or redesigned mounting is necessary to investigate.

The contact points move as casters swivel. For forward-aligned casters, nominal contacts are X = +0.23 m and −0.27 m; for reverse alignment, +0.27 m and −0.23 m. Therefore the support polygon is not fixed simply by mounting locations.

### Load distribution and stability

The original V1 support triangle has nominal contact points `(0, ±0.30)` and `(0.28, 0)` and area 0.084 m². Its centre of mass is near the rear support edge, motivating the new four-contact design.

V2 has a nominal diamond-shaped support polygon when all four wheels are in contact. Static equilibrium alone cannot uniquely determine all four normal loads; wheel compliance, mounting heights, preload and mass distribution matter.

For the hypothetical 30 kg, 60/40 drive-to-caster load case, each caster carries 58.86 N if equally loaded. With 0.02 m offset, the vertical-load bending moment is 1.1772 Nm.

## 6. New design requirement — suspension for safe food transport

I identified that small floor irregularities may spill food and drinks even if navigation succeeds. Suspension is therefore a functional requirement, not just a cosmetic addition.

The design should maintain wheel contact, reduce shock transmitted to trays, and avoid excessive body tilt. Springs store energy; dampers dissipate energy and reduce oscillation. Acceleration and jerk limits are also important because liquid can slosh even on a flat floor.

Independent suspension on all four wheels is a candidate architecture, not a final decision. A tall robot with a future arm may require additional roll and pitch control.

## 7. Spring mechanics and Hooke's law

For an ideal linear spring, the restoring force is `F = −kx` in signed coordinates. In compression calculations, its magnitude is `F = kx`.

- Stiffness `k` is measured in N/m (not mm).
- Static sag is displacement under stationary load.
- Suspension travel is the permitted movement range.
- Bottoming out occurs when the compression travel limit is reached.
- Spring energy is `E = ½kx²`.

### Preliminary spring sizing

Assume 30 kg total supported mass, 60% drive-wheel loading, 40% caster loading, equal loading within each pair, direct vertical springs, no preload, negligible unsprung mass and 10 mm target static sag.

| Wheel type | Static load per wheel | Candidate spring rate |
| --- | ---: | ---: |
| Powered wheel | 88.29 N | 8,829 N/m |
| Caster | 58.86 N | 5,886 N/m |

These rates are analytical examples. The actual spring load excludes unsprung weight and may depend on motion ratio and preload. The assumed load split is not guaranteed by spring rates alone.

### Independent exercise — 8 mm floor bump

Given: `k = 8000 N/m`, static load = 80 N, compression travel = 30 mm, bump = 8 mm. Assume no preload and a temporarily stationary chassis while the wheel rises.

| Question | My result | Assessment |
| --- | ---: | --- |
| Static compression | 10 mm | Correct |
| Compression after bump | 18 mm | Correct |
| Spring force after bump | 144 N | Correct |
| Remaining compression travel | 12 mm | Correct |

The additional force from the bump is 64 N.

I initially confused spring stiffness with compression in the conceptual question. Doubling stiffness does not double displacement. With the same load, static sag decreases.

| Parameter | Original spring | Doubled stiffness |
| --- | ---: | ---: |
| Stiffness | 8,000 N/m | 16,000 N/m |
| Static sag | 10 mm | 5 mm |
| Compression after 8 mm bump | 18 mm | 13 mm |
| Remaining compression travel | 12 mm | 17 mm |
| Spring force after bump | 144 N | 208 N |
| Additional spring force | 64 N | 128 N |

The stiffer spring leaves more compression travel in this scenario but creates a larger additional force for the same imposed wheel displacement. A soft spring risks excessive motion and bottoming out; a stiff spring can transmit larger shocks. Dynamic behaviour must be studied with damping, inertia and floor disturbances included.

## 8. ROS 2 / Gazebo integration plan

The existing motor control node publishes ROS 2 `Twist` messages to `/cmd_vel`. Gazebo's DiffDrive system accepts Gazebo Transport velocity messages. A `ros_gz_bridge` can connect them.

Suggested V1 command bridge (not newly validated during this study period):

```bash
ros2 run ros_gz_bridge parameter_bridge \
  '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist'
```

Suggested LiDAR bridge, assuming the actual Gazebo topic is `/lidar`:

```bash
ros2 run ros_gz_bridge parameter_bridge \
  '/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'
```

Check actual topics and types before running. The current LiDAR observation publisher uses hardcoded values; it is not yet processing real LaserScan messages. The full navigation stack should not be treated as sensor-driven until its placeholders are replaced and verified.

Proposed V2 joint chain: `base_link → suspension carrier (prismatic) → drive wheel (revolute)`. For a caster, a vertical suspension joint could precede the swivel joint and wheel rolling joint. The mounting mechanism, joint travel, stiffness, damping and controller compatibility remain to be implemented and tested.

## 9. Repository observations and pending fixes

The latest remote commit inspected was `bf0f9d383bfb75d4e76e17911d734b4622771741` (Restaurant_world, 11 November 2026). The local repository may be newer.

- V1 drive wheel collision thickness is 0.005 m but visual thickness is 0.05 m. V2 should use matching geometry.
- Some restaurant chairs have duplicate or incorrect positions; these need correction before navigation tests.
- The kitchen docking marker includes a 0.02 m collision platform. If it is only a floor marking, its collision should be removed; otherwise its threshold effect must be tested.
- V2 body, wheel suspension, casters, actual load distribution and integration are still pending. No V2 suspension performance results are claimed here.

## 10. Next steps and research direction

1. Study spring preload and its relationship to static sag and wheel contact force.
2. Study damping, sprung/unsprung mass, natural frequency and resonance.
3. Determine realistic suspension travel and load distribution for the four-contact platform.
4. Implement the V2 lower chassis, drive assemblies and casters in a separate SDF model.
5. Validate contact, traction, stability and turning before adding the standing body and payload.
6. Compare rigid, spring-only and spring-damper designs under identical simulated bumps. Record vertical acceleration, roll/pitch, contact forces, settling time, slip and odometry error. Later evaluate liquid sloshing or an appropriate payload-disturbance proxy separately.

My aim is to understand the mechanical and computational systems, develop them incrementally, and evaluate them experimentally rather than simply assemble a working demonstration.

