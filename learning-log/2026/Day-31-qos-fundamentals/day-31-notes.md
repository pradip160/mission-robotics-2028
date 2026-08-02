# Day 31 — ROS2 QoS Fundamentals

## Short Explain vedio link 
[https://youtu.be/TFavVR8AYFc]
## Session objective

Today I learned the meaning of ROS2 Quality of Service and applied one controlled QoS profile to the `/lidar_distance` publisher and subscriber.

## What QoS means

QoS controls how ROS2 messages are delivered between publishers and subscribers.

QoS is different from sensor freshness:

* QoS controls message delivery.
* Sensor freshness checks whether a received message is still recent enough to trust.

## QoS profile used

```python
sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5,
    durability=DurabilityPolicy.VOLATILE
)
```

### BEST_EFFORT

Lost LiDAR messages are not repeatedly retransmitted.

This is suitable for fast sensor streams because a new measurement normally arrives quickly and is more useful than retrying an old measurement.

### KEEP_LAST

ROS2 keeps only a limited number of recent queued messages.

### Depth 5

ROS2 can keep up to five queued messages. When a sixth message arrives, the oldest queued message is discarded.

### VOLATILE

A subscriber joining later does not receive messages published before it connected. It starts receiving newly published messages.

This is suitable for `/lidar_distance` because old distance readings may no longer represent the current environment.

## Publisher and subscriber compatibility

The `/lidar_distance` publisher and navigation subscriber both use:

```text
BEST_EFFORT
KEEP_LAST
Depth 5
VOLATILE
```

A publisher offering `BEST_EFFORT` cannot satisfy a subscriber requesting `RELIABLE`.

## Controlled runtime tests

The package compiled and built successfully.

```bash
python3 -m py_compile src/restaurant_robot_status/restaurant_robot_status/lidar_obstacle_publisher.py

python3 -m py_compile src/restaurant_robot_status/restaurant_robot_status/navigation_obstacle_subscriber.py

colcon build --packages-select restaurant_robot_status
```

QoS inspection confirmed:

```text
Publisher reliability: BEST_EFFORT
Subscriber reliability: BEST_EFFORT
Durability: VOLATILE
Publisher count: 1
Subscription count: 1
```

Compatible echo command:

```bash
ros2 topic echo /lidar_distance \
  --qos-reliability best_effort \
  --qos-durability volatile
```

This successfully received alternating values:

```text
0.6
3.0
```

## Intentional incompatible test

The echo subscriber was changed to request `RELIABLE`:

```bash
ros2 topic echo /lidar_distance \
  --qos-reliability reliable \
  --qos-durability volatile
```

ROS2 produced an incompatible QoS warning and delivered no messages.

The incompatible policy was:

```text
RELIABILITY
```

Changing the subscriber back to `BEST_EFFORT` restored communication.

## Main understanding

Fast sensor topics should prioritise recent information.

Discarding an old message from a live queue does not necessarily mean all useful information is lost. Processed information may remain in a map, and raw messages can be recorded separately when `rosbag2` recording is deliberately enabled.

A volatile subscriber is similar to a new member joining a WhatsApp group: it receives new messages after joining but does not receive messages published before it connected.
