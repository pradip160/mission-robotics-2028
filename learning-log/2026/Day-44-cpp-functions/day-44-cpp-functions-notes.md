Day 44 — C++ Functions for Robot Decisions

What I Learned

Created bool functions for robot safety checks.

Learned the difference between defining a function and calling it.

Used std::string when a function needs to return commands such as MOVE_FORWARD or TURN_LEFT.

Used void for a function that performs an action without returning a value.

Moved movement decision logic into a separate decide_movement() function.

Kept emergency and battery checks before movement decisions.

Functions Practised

is_battery_safe() → returns bool

is_emergency() → returns bool

decide_movement() → returns std::string

print_robot_command() → returns nothing (void)

Key Understanding

I already understood the decision logic, such as stopping for danger or choosing a clear path. Today I improved how to implement that logic correctly and cleanly in C++ using functions, parameters, return types, and function calls.

Learning Evidence

Worked on day40_cpp_basics.cpp and successfully reorganised the robot decision flow using functions.
