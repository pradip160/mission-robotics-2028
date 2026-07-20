## Day 22 - ROS2 Parameters and Runtime Saftey Configuration

Today I learned how to replace a hard-corded ROS2 saftey value with a configurable parameter. I also learned how to change the parameter while the node is running and reject unsafe values.

## Learning Evidence 

- YouTube video: [https://youtu.be/yox6sqSN-HQ]
- ROS2 package: `restaurant_robot_status`
- Practice workspace: /home/pradip/mission-korea/projects/ros2_ws

## Core Theory 

A ROS2 parameter is a configurable setting that belongs to node. it allows me to change robot behaviour without editing the source code every time.

Previously, the navigation node used a hard-coded timeout:

* `self.sensor_timeout = 3.0` 

This worked, but changing the timeout required editing the Python file and rebuilding the package.

By using a ROS2 parameter, the node now has:

- A safe default value of `3.0` seconds
- A value that can be inspected while the node is running 
- A value that can be changed at runtime
- Saftey validation that rejects zero or negative values

Parameters only exist while their node is running. When the node restarts, it loads its declared default again unless a configuration file provides another startup value.

## Implementation 

I replaced the hard-coded timeout wuth a declared ROS2 parameter:

`self.declare_parameter('sensor_timeout', 3.0`
`slef.sensor_timeout  = self.get_parameter('sensor_timeout').value`

The first line register `sensor_timeout` with a safe default of `3.0` seconds. 

The second line reads the current parameter value and stores it in the navigation node.

I also registered a runtime parameter callback.

`self.add_on_get_parameters_callback(self.parameter_callback)`

This callback allows the node to validate and apply a new timeout while it is still running.

## Runtime Saftey Validation

The parameter callback checks every requested parameter change.

For `sensor_timeout`, the value must be greater than `0.0`:

if parameter.value <= 0.0:
    return SetParametersResult(
        successful=False,
        reason='sensor_timeout must be greater than 0.0'
    )

If the value is valid, the navigation node updates its active timeout:

`self.sensor_timeout = parameter.value`

This is important because an unsafe timeout such as `0.0` could make sensor data become stale immediately and cause incorrect robot behaviour. 

The callback returns `successful=True` only after the requested value passes validation.


## ROS2 Parameter Commands

I used the following commands while the navigation node was running. 

List node's parameters:

`ros2 param list /navigation_obstacle_subscriber`

Read the current timeout 

`ros2 param get /navigation_obstacle_subscriber sensor_timeout`

Change the timeout to `1.0` second:

`ros2 param set /navigation_obstacle_subscriber sensor_timeout 1.0`
 
Test an unsafe value: 

`ros2 param set /navigation_obstacle_subscriber sensor_timeout 0.0`

ROS2 accepted `1.0`, but the callback rejected `0.0`.

## Test and Results 

I first confirmed that the running navigation node exposed the new parameter:

`sensor_timeout`

The declared defult value was:

`Double value is: 3.0`

I changed the value to `1.0` while the node was running: 

`Set parameter successful`
`Double value is: 1.0` 

I then tested the unsafe value `0.0`. The callback rejected it: 

`Setting parameter failed: sensor_timeout must be greater than 0.0` 

After the rejection, I checked the parameter again. IT remained at  the last valid value: 

`Double value is: 1.0`

This proved that an invalid request could not overwrite the active safe configuration. 

This full six-node robot system also continued responding to sensor information with commands such as `MOVE_FORWARD`, `TURN_LEFT`, and `STOP`.

Finally, I stopped the launch system with `CTRL-C`. Runnig `ros2 node list` produces no output, confirming that all robot nodes shut down cleanly. 


## What I Learned 

Today I learned that ROS2 parameter is setting owned by a running node.
 
Declare a parameter gives the node a recognised setting and a safe default value. Reading the parameter gives the Python program the value that it should use.
 
I also learned that reading a parameter only during startup is not enough when I want runtime changes.  parameter callback is needed to receive, validate, and apply a new value while the ode is running. 


Safety validation is important. The robot should not blindly accept every configuration value. Rejecting `0.0` prevented an unsafe timeout from replacing the last valid value.

I also learned that parameter changes made through the terminal are temporary. After the node restarts, it returns to its declared default. A YAML configuration file can later provide presistent startup values. 

Finally. I learned that dependencies used by the Python source code should also be declared in `package.xml`


## Personal Reflection 

Today I understood that robot saftey id not only about writing decision loguc. Configuration values can also affect how to sefely the robot behaves. 

Before this lesson, the sensor timeout was simply a fixed number inside the code. Now I understnad how ROS2 parameters make the system more felible while still keeping a safe default.

The most important part for me was learning that the robot should not accept every value blindly. When I tried to set the timeout to `0.0`, the node rejected it and kept the previous safe value. This showed me how validation protects the robot from unsafe configuration. 

I also improved my debugging process. Insted of trying to find one samll message inside a noisy six-node launch terminal, I used a seprate terminal to inspect the parameter clearly. 

This lesson made my navigation system more configurable safer, and closer to how a real ROS2 robot should be designed 

