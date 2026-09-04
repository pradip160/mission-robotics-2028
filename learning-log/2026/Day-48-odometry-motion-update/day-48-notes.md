# Day 48 — Differential-Drive Odometry Foundations

## Mission Korea 2028

### Today's Focus

Understanding how wheel motion changes a differential-drive robot's:

* center movement
* orientation
* x position
* y position

The goal was to understand the **physical meaning first**, not just memorize formulas.

---

## 1. Review: Robot Pose

For a 2D robot:

`pose = (x, y, θ)`

Where:

* `x` = position along the world's x-axis
* `y` = position along the world's y-axis
* `θ` = robot orientation / direction it is facing

Important:

**x and y tell us where the robot is.**

**θ tells us which way the robot is facing.**

Forward movement belongs to the robot, while x and y belong to the world coordinate frame.

---

## 2. Wheel Motion and Turning

For a differential-drive robot:

* Left wheel distance = Right wheel distance → robot moves straight
* Right wheel travels farther → robot curves left
* Left wheel travels farther → robot curves right

When the robot turns, `θ` changes.

Using the standard convention:

* left / counter-clockwise turn → positive `Δθ`
* right / clockwise turn → negative `Δθ`

---

## 3. Change in Orientation

The change in robot orientation is:

`Δθ = (Δs_R - Δs_L) / b`

Where:

* `Δs_R` = distance travelled by right wheel
* `Δs_L` = distance travelled by left wheel
* `b` = distance between the wheels (wheelbase)

### Physical meaning

The difference between the wheel distances determines how much the robot rotates.

A larger wheel-distance difference produces a larger change in orientation.

For the same wheel-distance difference:

* smaller wheelbase → sharper turn
* larger wheelbase → gentler turn

---

## 4. Updating Theta

Once `Δθ` is known:

`θ_new = θ_old + Δθ`

Example:

`θ_old = 0.8 rad`

`Δθ = +0.3 rad`

Therefore:

`θ_new = 1.1 rad`

Positive `Δθ` means the robot turned left.

---

## 5. Radians

Robotics commonly uses radians instead of degrees.

Useful reference values:

* `1 rad ≈ 57.3°`
* `1.57 rad ≈ 90°`
* `3.14 rad ≈ 180°`
* `6.28 rad ≈ 360°`

A radian connects angle with curved distance around a circle.

Radians are important because ROS2 and programming math functions commonly work with radians.

---

## 6. Robot Center Distance

The robot pose normally represents the center of the robot.

The center movement is estimated using the average wheel distance:

`Δs = (Δs_R + Δs_L) / 2`

Example:

Left wheel:

`Δs_L = 0.8 m`

Right wheel:

`Δs_R = 1.2 m`

Then:

`Δs = (0.8 + 1.2) / 2`

`Δs = 1.0 m`

So the robot center travelled approximately `1.0 m`.

### Important distinction

Average wheel movement tells us:

**how far the robot center moved**

Wheel-distance difference tells us:

**how much the robot rotated**

So:

`average → center movement`

`difference → rotation`

---

## 7. Converting Forward Movement into World x and y

The robot may move forward while facing different directions.

Therefore its center movement `Δs` must be separated into world x and y components.

The formulas are:

`Δx = Δs × cos(θ)`

`Δy = Δs × sin(θ)`

### Physical meaning

`Δx` = how much of the robot's movement happened along the world's x-axis.

`Δy` = how much happened along the world's y-axis.

---

## 8. Orientation Examples

### θ = 0°

Robot faces `+x`.

If it moves 1 m:

`Δx = +1 m`

`Δy = 0`

---

### θ = 90°

Robot faces `+y`.

If it moves 1 m:

`Δx = 0`

`Δy = +1 m`

---

### θ = 180°

Robot faces `-x`.

If it moves 2 m:

`Δx = -2 m`

`Δy = 0`

---

### θ = 45°

Robot faces diagonally toward `+x` and `+y`.

For a 2 m movement:

`cos(45°) ≈ 0.707`

`sin(45°) ≈ 0.707`

Therefore:

`Δx ≈ 1.414 m`

`Δy ≈ 1.414 m`

The robot still travelled only 2 m.

`Δx` and `Δy` are components of the same diagonal movement.

---

### θ = 135°

Robot faces toward `-x` and `+y`.

For a 2 m movement:

`cos(135°) ≈ -0.707`

`sin(135°) ≈ +0.707`

Therefore:

`Δx ≈ -1.414 m`

`Δy ≈ +1.414 m`

The negative x value means the robot moved toward the world's `-x` direction.

---

## 9. Current Odometry Chain

I can now connect the basic steps:

Wheel movement:

`Δs_L , Δs_R`

↓

Calculate robot center movement:

`Δs = (Δs_R + Δs_L) / 2`

↓

Calculate orientation change:

`Δθ = (Δs_R - Δs_L) / b`

↓

Calculate world movement:

`Δx = Δs cos(θ)`

`Δy = Δs sin(θ)`

↓

Update robot pose:

`x_new = x_old + Δx`

`y_new = y_old + Δy`

`θ_new = θ_old + Δθ`

---

## Learning Evidence

Today I understood:

* why unequal wheel movement changes θ
* why the robot turns toward the slower-moving wheel when both wheels move forward
* why a smaller wheelbase produces a larger rotation
* what `Δθ` physically represents
* why radians are used in robotics
* how average wheel distance estimates robot-center movement
* how `cos(θ)` and `sin(θ)` split forward movement into world x and y components
* why negative `Δx` or `Δy` represents movement in the negative world direction

I also corrected an important misconception:

`x` does not tell which way the robot is facing.

`θ` tells the robot orientation.

`x` and `y` describe its world position.

---

## Next Study Session

Continue from:

### Updating the Complete Robot Pose

Given:

* old `(x, y, θ)`
* left-wheel movement
* right-wheel movement
* wheelbase

calculate:

1. `Δs`
2. `Δθ`
3. `Δx`
4. `Δy`
5. `x_new`
6. `y_new`
7. `θ_new`

Then connect these calculations to actual ROS2 odometry and `/odom`.
