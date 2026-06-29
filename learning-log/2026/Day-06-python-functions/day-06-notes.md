Day 6: Python Functions for Robot Systems

Learning Evidence 

- Watch Day 6 Learning Vedio
  [https://youtu.be/zOynfdCHt-k] 

- Code: Day06_robot_functions.py
- Topic: Python functions for robotics systems

Goal 
the goal of Day 6 was to improve the Day 5 restaurant delivery robot monotoring logic by breaking the system into reusable Python functions. 

Insted of writing all robot decision in one long script, I started organize the robot system into smaller subsytems.

Functions Created
1. start_robot()
Purpose:
- Starts the robot missoin
- Display robot startup mission
- Shows that sensors are preparing
- Confirms the robot is ready

2. check_emergency_stop()
Purpose:
- Chcks weather emergency stop is active
- Returns True when emergency stop is pressed
- Returns Fasle when system is clear

Robotics lession:
Emergency stop has the highest priority.If it is active, the robot should stop immediately and should not continue to battery,obstacle, or movement checsk.

3. check_battery()
Purpose:
- Check the robot battery percentage
- Returns False when battery is low 
- Returns True when battery is safe

Robotics lession:
Low battery us not the same as emergency stop. A robot with low battery should return to the charging safely.

4. handle_obstacle()
Purpose:
- checks wheather an obstacle is detected
- Waits and scans again if the path is blokced
- Checks wheather the path becomes clear 
- Checks for an alternative route if thr path is still blocked
- Returns True if the robot has a safe path
- Returns False if no safe path is available

Robotics lesson:
An obstacle is usally recoverable.The robot should wait, scan again, and try an alternative route before pausing the mission.

5. move_robot()
Purpose:
- Checks distance to destination
- If distance is 0, delivery is complete
- If distanec is greater than 0, robot is still moving
- Returns True when delivery is complete
- Returns False when delivery is still in progress

Main Control Flow

The robot follows this priority order:
1. Start robot
2. Check emergency stop
3. Check battery saftey 
4. Handle obstacle
5. Move robot 
6. Decide delivery status

Important Lessons Learned 

- Functions definition created a resuable robot subsystem.
- Functions call actiavtes that subsystems.
- return sends a reasult back to the main control logic 
- retrun also ends the functions immediately.
- Main control logic decides which function should run next.
- Good variable names make logic easier to understand 
- path_safe is clearer than just obstacle.
- Emergency stop should block all lower-priority checks.
- Battery saftey should be checked before obstacle and movement.
- Robot movement should happen only after the path is safe.
- Delivery should be marked complete only when distance reaches 0.

Tests Completed 

Test 1: Emergency Stop

Input:
- Emergency stop:yes

Expected reasult:
- Mission stopped immediately
- Battery check did not run 

Status Passed

Test 2: Low Battery 

Input:

- Emergency stop:no
- Battery: 5

Expected reasult:
- Robot returns to charging station
- Obstacle and movement checks did not run 

Status: Passed

Test 3: Obstacle Recovery

Input:
- Emergency stop:no
- Battery: safe
- Obstacle detected: eys
- Path clear after scan:no
- Alternative route available: yes
- Alternative route safe: yes

Expected reasult:
- Robot follows alternative route
- Robot continue mission

Status Passed

Test 4: Delivery Complete 

Input:
- Emergency stop no
- Battery: safe
- Obstacle detected:no
- Distance to destination: 0

Expected reasult:
- Delivery completed

Status: Passed

Reflection

Today i learned how functions make robot code cleaner and easier to manage. I also learned that creating a function is different from calling a function. The robot system became easier to understand when eacg dunction had a one clear job.

This is important for robotics because real robot systems are made from many subsystems such as saftey, battery, obstacle handling,navigation, and delivery logic.
