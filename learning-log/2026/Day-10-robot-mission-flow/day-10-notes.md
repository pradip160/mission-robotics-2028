# Day 10: Robot Mission Flow / State Machine

## Learning Evdience 
- YouTube video: []
- Code file: projrct/ros2-restaurant-delivery-robot/control/Day10_robot_mission_flow.py
- Topic: Robot mission flow, state machine, mission report, and saftey logic 

## Goal 
Today i learned about how robot should handle its task and how it should keep record of the task it finished in logs. 

## What I Built:
Today i built simple but very important robot mission flow/ state machine:
- First out robot checks the order queue
- After finishing the checks it choose the best active order
- Robot runs the delivery mission
- Robot updates the order status
- And prints a final mission report 

## Mission States

The robot mission flow used these states:

- IDEL: robot is waiting for a mission
- SELECT_ORDER: robot selects the best active order 
- MOVING_TO_HALL: robot moves towards the customer table
- ARRIVED: robot reaches the target table
- DELIVERED: robot completes the delivery and updates order status
- IDEL: robot become ready for the next mission

## Mission Flow

IDEL → SELECT_ORDER → MOVING_TO_TABLE → ARRIVED → DELIVERED → IDEL

## Python Concepts Learned 

Today I practiced:

- functions
- if/ elif / else conditons
- dictionaries
- lists
- for loop
- while True loops
- return value
- break
- continue 
- indentation
- checking None safely

## What I Built

I built a system that does not only handle the task, but handles it smartly. The robot gives important to high-priority orders. If muntiple orders have the same priority, it checks the distance and choose the nearest table. The system also shows the robot's current state and records the mission path.


## Bugs I Fixed 

Today I Fixed serval bugs:

- Missing quote in f-string 
- 'order not defined' becasue code was outside the function 
- Wrong dictionary key, where table and order_id got mixed
- 'keyError' status' because one order dictionary was missing the status key
- Indentation mistake where the comparision logic was outside the for loop
- Spelling mistake in output such as IDLE
- Used return outside a function during solo practice 
- Missed colon after if conditon 


## ROS2 Connection 

Later, this logic can connect to ROS2.

- choose_next_order can connect to an order database or task manager node
- run_delivery_mission can connect to a navigation node
- MOVING_TO_TABLE can cannect to robot position or sensor confirmation
- DELIVERED can update the order status
- IDEL means the robot is waiting for the next mission


## Redlection

One week ago, I did not understand most if these ideas clearly. Today I built a robot mission flow using states, order decision logic, mision history, and saftey checks.

I learned that a robot should not only move, but should make safe decisions step byt step. I also learned that bugs are part of the learning process. Fixing errors helped me understand indentation, variable, dictionaries, and control flow better.

My next goal is to keep practicing small robotics cases by myself so I can build confidence and learn code more idependently.
