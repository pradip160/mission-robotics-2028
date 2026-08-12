# Day 37 — ROS2 Services: Robot Readiness Server and Client

## Goal

Learn how ROS2 services work and implement an on-demand robot-readiness check in the restaurant delivery robot.

## Topic versus service

A ROS2 topic provides continuous asynchronous communication.

Examples:

* Sensors continuously publish observations.
* Navigation continuously publishes motor commands and robot status.
* Subscribers receive messages whenever publishers send them.

A ROS2 service uses request-response communication.

Examples:

* A client asks whether the robot is ready.
* The server evaluates or retrieves the latest decision.
* The server sends a response directly to that client.

## Service roles

### Service server

The `navigation_obstacle_subscriber` node owns the `/check_robot_ready` service.

It is the correct server because it already owns the latest sensor states, freshness information, and navigation decision.

### Service client

The `robot_readiness_client` node sends a request to `/check_robot_ready`, waits for the response, and displays the readiness result.

## Service interface

The service uses:

```text
std_srvs/srv/Trigger
```

Its structure is:

```text
---
bool success
string message
```

The request is empty because the client does not need to provide input data. Calling the service already means “perform the readiness check now.”

The response contains:

* `success`: whether the robot is ready.
* `message`: the reason for the result.

## Server implementation

The navigation node creates the service using:

```python
self.create_service(
    Trigger,
    'check_robot_ready',
    self.check_robot_ready_callback
)
```

The callback returns the latest stored navigation result instead of duplicating all sensor conditions:

```python
response.success = self.robot_ready
response.message = self.readiness_reason
```

This creates one source of truth:

```text
Sensor data
→ navigation decision
→ motor command
→ robot-status topic
→ readiness-service response
```

## Python client flow

The client:

1. Creates a `Trigger` client for `/check_robot_ready`.
2. Waits until the server is available.
3. Creates an empty `Trigger.Request()`.
4. sends it asynchronously with `call_async()`.
5. Receives a future representing the response expected later.
6. Spins until that future is complete.
7. Logs the returned readiness result and reason.
8. Safely destroys the node and calls `rclpy.try_shutdown()`.

## Successful tests

### CLI service client

```bash
ros2 service call /check_robot_ready std_srvs/srv/Trigger "{}"
```

Stale-sensor response:

```text
success=False
message='One or more required sensors are stale'
```

Ready response:

```text
success=True
```

### Python client

```bash
ros2 run restaurant_robot_status robot_readiness_client
```

Successful output:

```text
Robot ready: True | Reason: Front obstacle detected; turning left through a clear path
```

### Unavailable-server test

When the navigation server was stopped, the client waited safely and repeatedly logged:

```text
Waiting for /check_robot_ready service...
```

It did not crash or send a request before the service became available.

## Topic and service snapshot behaviour

The `/robot_status` topic and `/check_robot_ready` service sometimes showed different reasons while both reported that the robot was ready.

This happened because new sensor messages arrived between the two terminal commands. Navigation recalculated its decision before the service request was sent.

Therefore, separate topic and service commands are snapshots taken at different moments.

## Debugging and fixes

### Workspace was not sourced

The package initially could not be discovered. Sourcing the workspace made the installed executables available:

```bash
source install/setup.bash
```

### Missing rear publisher

Both `/rear_status` and `/rear_distance` had zero publishers, causing `SENSOR_STALE`.

I inspected the topic endpoints and active node list, found that `rear_obstacle_publisher` was missing, and independently added it to the launch file.

After the fix, both rear topics had one publisher and one subscriber.

### Invalid recovery initialization

The navigation node contained:

```python
self.recovery_start_time = 'REVERSING'
```

This was invalid because `recovery_start_time` must contain either `None` or a ROS2 time object. The incorrect assignment was removed while the incomplete recovery transition remained safely inactive.

### Client indentation error

The service-waiting loop was accidentally placed at class level, where `self` did not exist. It was moved inside `__init__`.

### Naming and operator errors

The following errors were found and corrected:

* `RobotReadinessClint` → `RobotReadinessClient`
* `future - ...` → `future = ...`
* `robot_readiness_client:main` → `robot_readiness_client` in `ros2 run`
* incorrect package spelling during `colcon build`

### Hidden exception

Node creation originally failed before a logger existed, and the exception handler displayed nothing. The error handling was updated to use `print()` when the node has not yet been created.

## Dependencies and executable registration

Added to `package.xml`:

```xml
<exec_depend>std_srvs</exec_depend>
```

Added to `setup.py`:

```python
'robot_readiness_client = restaurant_robot_status.robot_readiness_client:main',
```

## Main lesson

A topic continuously distributes changing state, while a service handles a specific request and sends a direct response.

The service name identifies the correct communication endpoint, while the service type defines the request and response format shared by the client and server.

The readiness service does not create a second safety-decision system. It reports the latest decision already produced by the navigation node.
