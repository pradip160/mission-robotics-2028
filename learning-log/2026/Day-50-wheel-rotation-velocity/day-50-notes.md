# Day 50 — Radians, Wheel Rotation, Angular Velocity, and Linear Velocity

## Mission Korea 2028

### Today's Focus

Today I identified an important gap in my odometry foundation:

* radians and degrees
* wheel rotation
* angular velocity `ω`
* wheel radius
* linear wheel velocity
* how time connects wheel movement to odometry

The goal was to understand how a rotating wheel produces real movement along the ground.

---

## 1. Degrees and Radians

Angles can be represented using degrees or radians.

Important reference values:

* `180° = π rad ≈ 3.14159 rad`
* `360° = 2π rad ≈ 6.28319 rad`
* `90° = π/2 rad ≈ 1.57 rad`
* `45° = π/4 rad ≈ 0.785 rad`

A complete wheel revolution is:

`360° = 2π rad ≈ 6.28319 rad`

### Important terminology

* **radius** = physical size of the circle/wheel
* **radian** = unit used to measure an angle

These are different concepts.

---

## 2. Converting Degrees to Radians

Formula:

`radians = degrees × π / 180`

Example:

`90° × π / 180`

`= π / 2`

`≈ 1.57 rad`

---

## 3. Converting Radians to Degrees

Formula:

`degrees = radians × 180 / π`

Example:

`1 rad × 180 / π`

`≈ 57.3°`

Therefore:

`1 rad ≈ 57.3°`

---

## 4. Robot Orientation vs Wheel Rotation

Two different angles must not be confused.

### Robot orientation

`θ (theta)`

represents:

**which direction the entire robot is facing**

### Wheel rotation

`φ (phi)`

represents:

**how much the wheel itself rotated**

Example:

If one wheel completes one full revolution:

`Δφ = 2π rad`

or approximately:

`6.28319 rad`

---

## 5. Wheel Radius and Ground Distance

If a wheel rotates, its rotation can be converted into distance travelled along the ground.

Formula:

`s = rφ`

Where:

* `s` = wheel travel distance in metres
* `r` = wheel radius in metres
* `φ` = wheel rotation in radians

Example:

Wheel radius:

`r = 0.1 m`

One complete revolution:

`φ = 6.28319 rad`

Then:

`s = 0.1 × 6.28319`

`s = 0.628319 m`

### Physical Meaning

A wheel with radius `0.1 m` travels approximately:

`0.628 m`

along the ground when it completes one full revolution, assuming no wheel slip.

Important distinction:

* `0.1 m` → wheel radius
* `6.283 rad` → wheel rotation
* `0.628 m` → ground distance travelled

---

## 6. Angular Velocity — Omega

Angular velocity tells us how quickly the wheel angle changes with time.

Symbol:

`ω (omega)`

Formula:

`ω = Δφ / Δt`

Unit:

`rad/s`

Example:

Wheel rotates:

`6.283 rad`

in:

`2 seconds`

Then:

`ω = 6.283 / 2`

`ω ≈ 3.1416 rad/s`

### Physical Meaning

The wheel rotates through approximately:

`3.14 radians every second`

This is approximately half a revolution per second.

---

## 7. Linear Wheel Velocity

Angular velocity tells us how fast the wheel rotates.

Linear velocity tells us how fast the wheel moves along the ground.

Formula:

`v = rω`

Where:

* `v` = linear velocity in `m/s`
* `r` = wheel radius in metres
* `ω` = wheel angular velocity in `rad/s`

Example:

`r = 0.1 m`

`ω = 3.1416 rad/s`

Then:

`v = 0.1 × 3.1416`

`v = 0.31416 m/s`

### Physical Meaning

The wheel moves approximately:

`0.314 m`

along the ground every second, assuming constant speed and no slip.

---

## 8. One Revolution Per Second Example

If:

`r = 0.1 m`

and:

`ω = 6.28 rad/s`

then:

`v = rω`

`v = 0.1 × 6.28`

`v = 0.628 m/s`

This makes physical sense because:

`6.28 rad`

is approximately one complete revolution.

Earlier I calculated that one revolution of this wheel travels:

`0.628 m`

Therefore one revolution per second gives:

`0.628 m/s`

---

## 9. Distance and Time

If a robot travels:

`4 m`

in:

`3.8 seconds`

its average speed is:

`v = distance / time`

`v = 4 / 3.8`

`v ≈ 1.053 m/s`

This means the robot travelled approximately `1.053 m/s` on average.

However, this does NOT prove that it travelled exactly `1.053 m` during every individual second.

The robot may accelerate, slow down, or change speed during the movement.

---

## 10. Odometry Updates Over Time

A real robot does not normally wait several seconds before calculating its new pose.

It repeatedly performs small updates.

Example:

`0.0 s → read encoders`

`0.1 s → read encoders again`

Then:

1. calculate wheel rotation change
2. calculate wheel distances
3. calculate center movement
4. calculate orientation change
5. calculate `Δx` and `Δy`
6. update `(x, y, θ)`
7. repeat

This means odometry is calculated continuously over small time intervals.

---

## 11. Current Full Motion Chain

The relationship I am beginning to understand is:

Encoder measures wheel rotation

↓

`Δφ`

↓

Wheel radius converts rotation to distance

`s = rφ`

↓

Left and right wheel distances

↓

Robot center movement

`Δs = (Δs_R + Δs_L) / 2`

↓

Robot orientation change

`Δθ = (Δs_R - Δs_L) / b`

↓

World movement

`Δx`

`Δy`

↓

Update robot pose

`(x, y, θ)`

↓

Repeat after another small time interval

---

## Learning Evidence

Today I understood that:

* `360° = 2π rad ≈ 6.283 rad`
* radius and radian are completely different concepts
* `θ` represents robot orientation
* `φ` can represent wheel rotation
* one complete wheel revolution is `2π rad`
* wheel rotation can be converted to ground distance using `s = rφ`
* `ω` represents angular velocity in `rad/s`
* angular velocity tells how quickly the wheel rotates
* linear wheel velocity can be calculated using `v = rω`
* odometry operates through repeated measurements over small time intervals

I also made and corrected decimal multiplication mistakes while calculating wheel velocity.

---

## Next Study Session

Start with a short recap of:

1. degrees and radians
2. `θ` vs `φ`
3. `s = rφ`
4. `ω = Δφ / Δt`
5. `v = rω`

Then continue into:

### Encoder Measurements Over Time

Understand how:

`encoder ticks → wheel rotation → wheel distance → wheel velocity → robot velocity → pose updates`

and how the robot estimates its pose repeatedly every small time step.
