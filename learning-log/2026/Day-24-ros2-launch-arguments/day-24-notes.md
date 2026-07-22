## Day 24 - ROS2 Launch Arguments 

## Learning Goal 

The goal of Day 24 was to learn how ROS2 launch arguments allow me to provide a temporary parameter value when starting the robot system. I used a launch argument to change `sensor_timeout` without editing the YAML configuration file or the navigation node. 

## System Design 

The launch file now declares a launch argument called `sensor_timeout` with a default value of `4.0`. 

The selected launch value is read using `LaunchConfiguration` and converted into a float using `ParameterValue`. The navigation node first loafs the YAML configuration file and then receives the launch argument as an override. 

The value flos is: 

Launch command 
- DeclareLaunchArgument
- LaunchConfiguration
- ParameterValue as float
- navigation_obstacle_subscriber

If no argument is supplied, the system uses `4.0`. If I launch with `sensor_timeout:7=0`, the navigation node uses `7.0` only for that launch session.

## Implementation 

I imported the launch tools required to create and use the argument:

``` 
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue
```
I declare the launch argument inside `LaunchDescription`:

```
DeclareLaunchArgument(
    'sensor_timeout`,
    default_value='4.0'
    description='Maximum sensor message age before it becomes stale' 
),```

I then read the selected launch value: 

`sensor_timeout = LaunchConfiguration('sensot_timeout')`

Because launch arguments begin as text-like values, I converted the selected value into a float: 

``` 
sensor_timeout_value = ParameterValue(
    sensor_timeout,
    value_type=float
)
```

Finally, I passed both parameter sources to the navigation node: 

``` 
parameter=[
    config_files,
    {'sensor_timeout': sensor_timeout_value}
],
```
The YAML file loads first, and the launch value is applied afterward as a temporary override. 

## Testing and Reasults


I first checked that the launch argument was registered correctly: 

``` 
ros2 launch restaurant_robot_status restaurant_robot_system.launch.py --show-args
```
ROS2 displayed: 
```
'sensor_timeout':
    Maximum snesor message age before it became stale 
    (default: '4.0')
```
I then launched the system without provoding an argument:

`ros2 launch restaurant_robot_status restaurant_robot_system.launch.py`

In another terminal, I cheked the parameter: 

`ros2 param get /navigation_obstacle_subscriber sensor_timeout`

The reasult was: 

`Double value is: 4.0`

Next, I launched the system with a temporary override: 

``` 
ros2 launch restaurant_robot_status restaurant_robot_system.launch.oy sensor_timeout:=7.0
```
The parameter checked returned: 

`Double value is:7.0`

After stopping the system and  launching again without an argument, the value returned to `4.0`. 

This confirmed that the launch argument overrides the default only for the current launch session and does not permanently change the YAML configuration. 

 

## What I Learned 

Today I learned that a launch argument is a vlaue supplied when starting a ROS2 system. In this case,`sensor_timeout` is the argument name and `7.0` is thr calue provided to it. 

I learned the difference between a saved parameter value and a temporary launch override. The YAML file keeps the normal value of `4.0`, while the launch argument can temporarily provide another value for one startup.

I also learned that: 

- `DeclareLaunchArgument` makes an argument available to the launch system. 
- `LaunchConfiguration` reads the selected argument value. 
- `ParameterValue` ensure that the value is passed using the correct data type. 
-  Parameter source order matters because the later value can override an earlier YAML value.
- `py_compile` checks Python syntax but may not detect an incorrect import name. 
- The package must be rebilt after changing a launch file because ROS2 uses the installed copy. 

## Personal Reflection

At first, I was confused about what an argument meant. After testing the default value, the temporary override, and then restarting the system, I understood it clearly. 

An argument is a startup instruction. It lets change hoe the robot starts without changing the saved configuration. 

I also rebuilt the same feature in the main portfolio package after practising it first. This healped me recall the structure instead of only copying it. 


