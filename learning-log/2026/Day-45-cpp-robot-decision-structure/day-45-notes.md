# Day 45 — C++ Robot Decision Structure

## What I Learned

* Used functions to separate robot responsibilities:

  * `is_battery_safe()`
  * `is_emergency()`
  * `decide_movement()`
  * `decide_robot_command()`
  * `print_robot_command()`
* Simplified `main()` so it only creates the robot state, requests a command, and prints it.
* Learned the basic concept of a C++ `struct`.
* Created a `RobotState` struct containing:

  * battery percentage
  * obstacle distance
  * left path
  * right path
  * emergency status
* Created one `RobotState robot` object and accessed its values using `robot.variable_name`.

## Current Result

The program successfully outputs:

`MOVE_FORWARD`

## Next Step

Modify `decide_robot_command()` so it receives the entire `RobotState` object instead of five separate arguments.
