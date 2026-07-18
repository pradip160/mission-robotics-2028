# Day 21 - ROS2 Launch Files
- YouTube Link [https://youtu.be/kIo4fY9MS5c]

## Learning Context 
Today I learned how to use a ROS2 Python launch file to start muntiple nodes together with one command.

I completed this lesson inside my seprate practice workspace:
`/home/pradip/mission-korea-day20-practice/ros2_ws`

Practice package:

`restaurant_robot_practice`

The practice workspace is my tranning area, while the notes are stored in my main Mission Korea repository as learning evdience.

## Learning Objectives

- Understand the purpose of ROS2 launch file.
- Create a Python launch file for a multi-node robot system.
- Install the launch file correctly through `setup.py`.
- Start six ROS2 nodes using one command and terminal.
- Insepct the running nodes and topics.
- Shut down the complete robot system safely using `Ctrl+C`.


## Why ROS2 Launch Files Matter 
Opeaning  separate terminal for every node is inconvenient and increase the chance of human error. An operator may forgot to start one sensor, close the wrong terminal, or start an incomplete robot system. 

A ROS2 launch files allows muntiple nodes to start together using one command. This makes the robot systemt to operate, inspect, test, and  shut down. 

The launch file only starts and organise nodes. It does not replace the safety logic inside the navigation node. Missing stale, or unknown sensor data must still cause the robot to stop. 

## Robot System Architecture

The launch file starts the following six ROS2 nodes:

* `camera_obstacle_publisher`
* `lidar_obstacle_publisher`
* `left_obstacle_publisher`
* `right_obstacle_publisher`
* `navigation_obstacle_subscriber`
* `motor_control_subscriber`

The four sensor publishers send information to the navigation node through separate ROS2 topics.

The navigation node checks the sensor states and their freshness before publishing a command through `/motor_command`.

The motor-control subscriber receives the command and converts it into simulated wheel behaviour.

```text
Camera ──┐
LiDAR ───┤
Left ────┼──> Navigation ───> /motor_command ───> Motor control
Right ───┘
```

## Launch File Structure

I created a `launch` directory at the package root:

* `restaurant_robot_practice/launch/`

The Python launch file is:

* `restaurant_robot_system.launch.py`

The launch file imports: 
- `LaunchDescription` to hold the complete startup plan. 
- `Node` to represent each ROS2 node that should start. 

The required function is: 
* `generate_launch_description`

ROS2 calls this function when I run ros2 launch. The function returns a `LaunchDescription` containing all six node actions.

## Launch File Installation 

Create the launch file inside the source package was not enough.I also ipdated `setup.py` so that `colcon` installs the launch file where ROS2 can discover it.

I imported:

* `from glob import glob`

I then added the launch-file installation path inside `data_files`.

I also added the following runtime dependency to `package.xml`:
* `<exec_depend>ros2launch</exec_depend>`

After thsese changes, I built and sourced the workplace before running the launch file. 

## Command Used

I built the package with:

* `colcon build --packages-select restaurant_robot_practice`

I sourced the workplace with:

* `source install/setup.bash`

I started the complete robot system with:
* `ros2 launch restaurant_robot_practice restaurant_robot_system.launch.py

I inspected the running system using:

* `ros2 node list`
* `ros2 topic list`

Testing Reasults

Test 1 -- Compelte System Startup

Action: Ran the Python launch file using one `ros2 launch` command. 
Reasult: All six robot nodes started successfully.
Status: Passed

Test 2 -- Node Inspection 

`ros2 node list` showed:
* `/camera_obstacle_publisher`
* `/lidar_obstacle_publisher`
* `/left_obstacle_publisher`
* `/righ_obstacel_publisher`
* `/navigation_obstacle_subscriber`
* `/motor_control_subscriber`

Status: Passed

Test 3 -- Topic Inspection 

`ros2 topic lists` showed:
* `/obstacle_status`
* `/lidar_status`
* `/left_status`
* `/right_status`
* `/motor_command`

It also showed the ROS2 internal topics `/paramater_eventd` and `/rosout`.

Status: Passed 

Test 5 -- Complete System Shutdown

Action: Pressed `Ctrl+C` in the launch terminal.

Reasult: All six nodes finished cleanly without leaving any robot nodes running. 

A final `ros2 node list` command return no active nodes. 

Status: Passed


## Debugging Notes 

1. Incorrect Launch Directory Name

I accidentally created a directory name `lunch` insted of `launch`.

I correctd it using: 
`mv lunch launch`

This taught me that ROS2 and linux require exact names.

2. Launch File and Spelling Errors

I initially misspelled:
* `LaunchDescription`
* `generate_launch_description()

ROS2 requires the exact function name `generate_launch_description()` to load a Python launch file. 

3. Incorrect Node Structure

While adding nodes, I made several samll mistakes:

* Forgot to write `Nodes(` before one node entry.
* Used `executables` insted of `executable`.
* Added the navigation node twice.
* Used `motor_commabd_subscriber` insted of the register executable name `motor_control_subscriber`

I corrected each error by checking the launch-file structure and comparing executables names with `setup.py`

4. Launch File Not Installed Automatically

The launch file existed inside the source package, but ROS2 also needed it to be installed. 

I added `glob` and updated the `data_files` section in `setup.py` so that the launch file was installed under the package's `share` directory. 

5. Shutdown Tracebacks

Durning the first `Ctrl+C` test, several nodes printed `KeyboardInterrupt`
tracebacks because their `main()` functions did not handle shutdown safely. 

I added:

* `try`
* `except KeyboardInterrupt`
* `finally`
* `node.destroy_node()`
* `rclpy.try_shutdown()`

The use of `rclpy.try_shutdown() prevented an error when the ROS2 context had already been shutdown. 

6. Source Code and Installed Cose

After editing a node, ROS2 sometimes continues runnig the older installed version.

I learned that changing ROS1 Python source code, I must:
- 1. Build the package.
- 2. Source `install/setup.bash`
- 3. Run the node or launch file again.

After rebuilding and sourcing, all six nodes shut down cleanly. 
	
## What I learned

I learneda new way to start ROS2 nodes by using a ROS2 launch file. Before this lesson, I had to run every node separateltely in different terminals. After creating the launch file, I can now start and stop all six robot nodes at the same time using one command. 

I also learned how to shut down ROS2 nodes cleanly. Previously, pressing `Ctrl+C` produced long traceback messages. After using `try`, `except`, and `finally`, together with `node.destroy_node()` and `rclpy.try_shutdown()`, all my nodes can now stop cleanly without displayong unnecessary error messages. 

I improved my understanding of important ROS3 and Linux commands. I now understand how to run a node using `ros2 run <package> <executable>, build a package using `colcon build -- packages-select <package>, and source the workspace using `source install/setup.bash`. I also understand `setup.py`
more clearly, including how it registers executables nodes and installs launch files so ROS2 can discover them. 

Most importantly , I understand more about how ROS2 cancepts connect to a real robot. Althrough my restaurant delivery robot is currently simulated, its sensor,navigation, and motor-control architecture could later control physical hardware with further development. Seeing the complete system communicate successfully encouraged me to continue learning and improve my robotics skills.

## Personal Reflection 

I felt relieved and amazed when I saw how important and useful a ROS2 launch file can be. It reduces human error because I no longer need to open a new terminak for every node and cehck each one separately. Now i can start my entire robot system from one terminal using one command. 

The shutdown tracebacks were the most frustrating part of today's lesson. I tried several methods to fix them, but the problem remained. From this, I learned one very important lesson: whenecer I change ROS2 source code, I must rebuild the package and source the workspace again. Otherwise, ROS2 may continue running the previously installed version of the code. 

When I finally corrected the shutdown loguc and all six nodes stopped cleanly, I felt happy and proud of myself. It proved that I can solve difficult problems by continuing to test,observe, and improve my work.

I also learned something important about my mindset. When I want to achieve something, I must try even when I am starting from zero and do not fully understand it yet. If I decide that I cannot do something before trying, I lose immediately. However, If i try, there are two possible result: I succesed or I make a mistake and gain knowladge from it. 

Therefore, there is no real loss in trying to move towards success. Ths is one of the main reason Why i continue learning robotics.
