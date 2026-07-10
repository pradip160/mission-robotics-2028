# Day  15: ROS2 Muntiple obstacle states and navigation decisions

## Learning Evidence 

- YouTube video: [https://youtu.be/-N8AyMIDOLM]
- Package: `restaurant_robot_status`
- Publisher: `camera_obstacle_publisher`
- Subscriber: `navigation_obstacle_subscriber`
- Topic: `/obstacle_status`

## Goal

My goal was to improve the Day 14 obstacle communication system. On Day 14, the robot only puvlished and reacted to one message, so it did not feel like it was performing different tasks. Today,I added and tested muntiple conditions, including `OBSTACEL_DETECTED`, `PATH_CLEAR`, and `PERSON_DETTECTED`. This ,ade the navigation subscriber react differently depending on the message it received and made the system feel more like robot decision-making.

## Why Robots Need Muntiple States 

Robot need muntiple states because they need to perform different actions in different scenarios. For example, the robot should stop and change direction when an obstacle is detected, continue navigation when the path is clear, and stop and wait when a person is detected. Without muntiple states, the robot would react in the same way to every situation.

## Publisher Changes
Inside the publisher, I added conditions so it could send differet messages to the subscriber. I used `self.obstacle_present` to remember the current simulated obstacle state. When the value is `True` the publisher sends `OBSTACLE_DETETCTED` and when it is `False`, it sends `PATH_CLEAR`. After publishing each message, the boolean value is reversed so the two states alternate. 

## Subscriber Changes
Inside the navigation subscriber, I added different conditions to decide how the robto should react to each message. If it receives `OBATACLE_DETECTED`, it decides to stop and change `PERSON_DETECTED`, it stops and waits. I also added an else condition so the robot stpos safely when it receives an unknown message.


## Testing and Reasults

I tested the system by checking whether both nodes were working correctly. I ran the camera publisher in one terminal and the navigation subscriber in another terminal. I confirmed that the publisher sent different messages and that the subscriber reacte correctly to each one.
I also uded `ros2 node list` to conform that both nodes were running. Then I used `ros2 topic echo /obstacle_status` to create a temporary subscriber and inspect the message travelling through the topic. I Learned that the publisher did not need a  new program or a separate topic to send different messagge values.
Using `ros2 topic info /obstacle_status`, I saw the subscription count increase from one to two while `ros2 topic echo` was running. This showed that `ros2 topic echo` temporarily acts as another subscriber.


## Manual Message Testing

I manually published `SENSOR_ERROR` through the existing `/obstacle_status` topic. Because this value did not match any recognised condition, the subscriber entered the `else` branch and showed a warning that the robot should stop for safety. This confirmed that the fail-safe behaviour was working correctly.

I also manually published `PERSON_DETECTED`. The navigation subscriber matched the new `elif` condition and logged that the robot should stop and wait. These tests showed that one topic can carry different message values and that the subscriber can make different decisions depending on the received state.

## What I Learned

Today, I learned that one ROS2 publisher can send different message values through the same topic. I also learned that the subscriber can use `if`, `elif`, and `else` conditions to make different navigation decisions.

I understood that message values must match exactly, including spelling, capitalisation, underscores, and spaces. If the message does not match any known condition, the `else` branch handles it safely.

I also learned that the publisher reports what it senses, the navigation node decides what action is needed, and a future motor-control node will physically control the wheels. This helped me understand how separate ROS2 nodes can work together as parts of one robot system.
