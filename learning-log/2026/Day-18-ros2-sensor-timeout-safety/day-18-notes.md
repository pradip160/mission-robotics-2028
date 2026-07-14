## Learning Evidence

- **YouTube Video:** [https://youtu.be/PdUlFRLN1NU]
- **ROS2 Package:** `restaurant_robot_status`
- **Main Code File:** `navigation_obstacle_subscriber.py`
- **Topic:** ROS2 sensor timeout, stale-data detection, and safe navigation decisions
- **Test Evidence:** The robot published `STOP` when either the camera or LiDAR stopped sending fresh data for more than three seconds.

## Goal

To make the navigation node detect missing or stale camera and LiDAR data, stop the robot when sensor information is unsafe, and only allow movement when both sensors are fresh and report `PATH_CLEAR`.

## Testing and Reasults

First, I tested the system by running only the camera obstacle publisher and the navigation subscriber nodes. The robot continued to send a `STOP` command even when the camera reportd `PATH_CLEAR`, because the robot requires both the camera and LiDAR to report before it can move forward. 

If either sensor reports `OBSTACLE_DETECTED`, the robot stops bacause uncertanity can be dangerious in robotics. I also stopped the camera obstacle publisher while the system was running. The navigation node still displayed the camera's last publishing state, but it correctly send a `STOP` command even through the last message was `PATH_CLEAR`.

The robot treats any sensor message older than three secounds as stale and does not act on it. 

## Implementation

I added a three-second sensor timeout and created a safety timer inside `__init__`. The value `sensor_timeout = 3.0` means that sensor data received within three seconds is considered fresh, while data older than three seconds is considered stale.

The safety timer runs every second and checks whether new camera and LiDAR messages have been received recently. The node calculates the age of each sensor message by subtracting the time when the last message was received from the current ROS2 time.

If either the camera or LiDAR data is missing or stale, the navigation node publishes a `STOP` command. The robot only publishes `MOVE_FORWARD` when both sensor messages are fresh and both sensors report `PATH_CLEAR`.


## Inspection 

At first, my nodes were not working correctly, so I inspected the code and discovered that I had forgotten to add the saftey timer inside `__init__`. After adding the timer, I found another bug inside `decide_navigation()`. I had used two separate `if` statements, which allowed the later conditions to overwrite  the `STOP` command with`MOVE_FORWARD` even after one sensor stopped publishing.

I changed the secound `if` statement to `elif` so that once the robot choose `STOP` because of stale sensor data, the later conditions cannot replace that saftey decision. I also discovered that I had accidentally defined `check_sensor_freshness()` twice, so I removed the duplicate unfinished function. 

After correction the code, I checked the syntax, rebuilt the ROS2 package, spurced the workspace, and restarted the nodes. The final test proved that the system was working properly. The robot no longer made decisions only from the latest stored sensor state; it checked whether the sensor data had arrived within the allowed timeout before deciding whether it was safe to move. 


## Personal Reflection

I felt very emotional and motivated when I saw my small simulated robot making decisions based on sensor inputs. I learned that stale sensor data can be dangerous if a robot makes decisions using outdated information. A robot should avoid trusting old or missing sensor data because uncertainty in robotics can lead to serious and expensive mistakes.

I also learned that I should not define the same function twice. Another important lesson was that `if` and `elif` are not the same. If I use a separate `if` instead of `elif`, Python may continue checking later conditions and overwrite an earlier safety decision, which could cause the robot to move when it should stop.

This task brought me one step closer to building a robot that can move safely and make careful decisions in a real room.


## Day 18 Summary 
Today i improved the safety of my ROS2 restaurant delivery robot by adding sensor timeout and freshness checking. The navigation node now records when the latest camera and LiDAR messages are received and checked their age every second. 

The robot only moves forward when both sensors provides fresh data and both report `PATH_CLEAR`.If either sensor reports an obstacle, stops publishing, or provides data older than three seconds. the robot sends a `STOP` command. 

I also debiugged two important problems: a separate `if` statement was overwriting the safety decision,and `check_sensor_freshness()` had been defined twice. After fixing these issues, rebuilding the package, and testing the nodes, the robot correctly stopped when sensor information became stale.
