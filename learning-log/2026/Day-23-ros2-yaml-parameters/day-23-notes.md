## Day 23 -- ROS2 YAML Parameter Files 

## Learning Evidience 

- Github
- YouTube:[]

## Learning Objective

Today I learned how to save ROS2 parameter values inside a YAML configuration file. 

Previously, I changed sensor_timeout using the `ros2 param set` command. That change only affected the currently running node and dissapered after the node restarted. 

My goal was to load `sensor_timeout: 4.0` automatically whenever the navigation node starts. 

## Core Theory 

A ROS2 parameter is a configurable value used by a node.

For example, the navigation node uses:

`sensor_timeout`

This value decides how old a sensor message can become before the robot treats it as stale.

There are two ways I used parameters: 

`ros2 param set`

This changes the value only while the node is running.

`yamal parameter file` 

This stores the value in a file and loads it again whenever the node starts.

A YAML file is therefore like a saved configuration sheet of the robot.


## YAML File Structure

I created this configuration file:

``` navigation_obstacle_subscriber:
        ros__parameters:
            sensor_timeout: 4.0
```
The first line identifies the ROS2 node:

`navigation_obstacle_subscriber`

The `ros__parameters` section tells ROS2 that the values below it are parameters for that node.

The final line sets:

`sensor_timeout = 4.0 seconds`

The node name and the double underscore in `ros__parameters` must be written exactly. Spelling mistake can prevent ROS2 from loading the parameter.

## Testing and Reasults

I first tested the YMAL file directly with the navigation node: 

```
--ros2-args\
--params-file src/restaurant_robot_practice/config/navigation_params.yaml
```
I then checked the loaded parameter:
`ros2 param get /navigation_obstacle_subscriber sensor_timeout`

The reasult was:
 
`Double value is: 4.0

Next, I rebuilt the package and comfirmed that the YAML file was installed: 

``` ls install/restaurant_robot_practice/share/restaurant_robot_practice/co
fig ```

The installed file was: 

`navigation_params.yaml`

I then updated the launch file so it loaded the YAML configuration automatically.

After launching the complete six-node robot system, I checked the parameter again: 

`ros2 param get/navigation_obstacle_subscriber sensor_timeout`

The result remained:

`Double value is: 4.0`

This proved that the launch file correctly found the installed YAML file and loaded the saved parameter without requiring a manual `--params-file` command. 

## Errors and Debugging 

While creating the YAML file, I made several spelling mistakes.

I first wrote the node name incorrectly: 

`navigation_obstaclce_subscribe`

The correct node name was: 

`navigation_obstacle_subscriber`

I also wrote:

`ros_parameters`

insted of the required ROS2 key: 

`ros__parameters`

The double underscore was important 

While updating `setup.py`, I also made mistakes such as: 

`pakage_name`

insted of:

`package_name`

I used this command to check the python syntax:

`python3 -m py_compile setup.py`

I also checked the launch-file syntax with: 

`pyhton3 -m py_compile launch/restaurant_robot_system.launch.py`

Another error occurred in the launch file because I defined: 

`config_file`

but later used:

`config_files`

The extrs `s` caused a `NameError`.
After correcting the variable name, rebuildinf the package and sourcing the workspace again, the launch system started successfully.

I learned that successful Python compilation does not guarantee that every runtime variable name is correct. Some errors only appear when the launch file actually runs. 


## What I Learned

Today I learned the difference between a temporary ROS2 parameter change and a saved parameter configuration. 

The command: 

`ros2 param set /navigation_obstacle_subscriber sensor_timeout 4.0`

changes the value only inside the currently running node. When the node stops, that temporary value is lost.

A YAML file stores the configuration so the same value can be loaded every time the robot starts.

I learned that the YAML structure must match the exact ROS2 node name:

``` navigation_obstacle_subscriber: 
        ros__parameters:
            sensor_timeout: 4.0
```

I also learned that creating a YAML file inside the source package is not enough. The file must be included in `setup.py` so colcon build installs it with the package. 

The launch file can then use `get_package_share_directory()` to find the installed package insted of depending on a fixed computer path.

This makes the robot package more portable. Another computer can install the package and the launch file can still locate its configuratiom. 

I also learned the complete configutation flow: 

YAML source file 
- setup.py install it 
- launch file finds it
- navigation node loads it
- sensot_timeout becomes 4.0


## Personal Reflection 

Today I understood why professional robot systems seperate configuration
form Python code. 

The Python node contains the robot's behaviour, while the YAML file contains values that my need to change for different enviroments.

For  example, the navigation logic can remain unchanged while the sensor timeout is adjusted for a faster or slower sensor system.

I also improved my debugging skills. Small spelling mistakes in node names, YAML keys and Python variables caused different types of errors. I checked each layer separately:

YAML structure
→ Python syntax
→ package installation
→ launch execution
→ parameter value

This helped me understand that robotics debugging should be systematic. I should not randomly change many lines at once. I should test one part of the system, confirm it works and then continue.

## Day 23 Summary

Today I successfully:

Created a ROS2 YAML parameter file.
Stored sensor_timeout: 4.0.
Installed the YAML file through setup.py.
Found the installed file using get_package_share_directory().
Connected the YAML file to the navigation node.
Loaded the configuration automatically through the launch file.
Verified the value using ros2 param get.
Repeated the complete process in both the practice and main robot packages.

The main robot can now start with a saved sensor timeout configuration without requiring a manual parameter command.
