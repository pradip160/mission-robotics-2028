# Day 46 – C++ Robot Commands with `enum class`

## What I Learned

Today I improved the beginner robot decision system by replacing string commands with safer C++ enum commands.

### Robot State

I used a `RobotState` struct to store:

* battery percentage
* obstacle distance
* left path status
* right path status
* emergency status

### `const RobotState&`

I changed the decision function to:

```cpp
RobotCommand decide_movement(const RobotState& robot)
```

* `&` means the function uses the existing robot state instead of copying it.
* `const` means the decision function cannot modify the robot state.

I tested this by trying to change `robot.battery_percentage`, and the compiler correctly rejected it as a read-only object.

### `enum class RobotCommand`

I created:

```cpp
enum class RobotCommand
{
    EMERGENCY_STOP,
    LOW_BATTERY_STOP,
    MOVE_FORWARD,
    TURN_LEFT,
    TURN_RIGHT,
    PATH_BLOCKED_STOP
};
```

This is safer than strings because invalid commands can be caught by the compiler.

### Robot Decision Priority

1. Emergency → `EMERGENCY_STOP`
2. Low battery → `LOW_BATTERY_STOP`
3. Front clear → `MOVE_FORWARD`
4. Left clear → `TURN_LEFT`
5. Right clear → `TURN_RIGHT`
6. All paths blocked → `PATH_BLOCKED_STOP`

### Printing Commands

Because `std::cout` cannot directly print an `enum class`, I used:

* `switch`
* `case`
* `break`

inside `print_robot_command()`.

## Result

The program compiled successfully and printed:

```text
TURN_LEFT
```

## C++ Concepts Practised

* `struct`
* functions
* `const`
* references `&`
* `enum class`
* `switch`
* `case`
* `break`
* compiler type checking

## Learning Evidence

Successfully converted the robot decision system from string commands to strongly typed `RobotCommand` enum values and tested the program successfully.
