# Day 9: Robot Order Decision Logic

## Learning Evidence
- YouTube video: [https://youtu.be/ZtxAZY87UUk]
- Code file: projects/ros2-restaurant-delivery-robot/control/Day09_robot_order_decision.py
- Topic: Priority-based robot order decision logic

## Goal
Today I improved my restaurant delivery robot so it can choose which order to deliver first.

## What I Built
I built a function called choose_next_order(orders).

This function checks the robot order queue and chooses the best order using priority and distance.

## Robotics Meaning
In robotics, the robot should not just store data. It must make decisions.

For a restaurant delivery robot, choosing the next order is important because some orders may be urgent and some tables may be closer.

## Decision Rules
The robot follows these rules:

1. Skip delivered and cancelled orders.
2. Choose high priority before normal priority.
3. Choose normal priority before low priority.
4. If two orders have the same priority, choose the nearer table.

## Python Concepts I Practiced
- dictionaries
- lists
- functions
- for loops
- if / elif / else
- None
- continue
- comparison operators
- priority ranking dictionary

## Bugs I Faced
- I edited the Day 8 file by mistake.
- I had trouble saving and exiting nano.
- I got confused with indentation.
- I got `orders is not defined`.
- I got `next_order is not defined`.
- I learned that function calls must happen after the data is created.

## What I Learned
I learned that:

- define function means prepare robot skill
- call function means use robot skill
- best_order stores the current best robot mission
- priority words need to be converted into numbers
- robot software must handle empty/no-active mission cases safely

## Final Result
The robot successfully selected the best order using priority first and distance second.

When all orders were delivered or cancelled, the robot safely printed that there were no active orders available.
