# Day 5: Robot Monitoring loop
# Learning vedio
[Watch Day 5 Learning Vedio]
[https://youtu.be/UipmwwyBbjs]
## Mission Korea Robotics Journey 

Today I learned how to use Python while loops to simulate a restaurant delivery robot saftey and mission status during a delivery task.

## What i built

I built a robot monotoring loop that keeps checking robot saftey and mission status during a delivery task.

## Concepts learned

- while loop for continious monitoring 
- break to stop the robot immediately
- continue to return to the next monitoring cycle
- emergency stop pirority 
- battery saftey logic
- obstacle detection 
- obstacle recovery 
- alternative route decision
- distance-to-destination logic
- delivery status conformatio 
- delivery counter 

## Robot saftey order
- Emergency stop 
- Batteryy levl
- Obstacle detection
- Alternative route check
- Distance to destination information
- Delivery status
- Return to base

## Important lession
A robot should not only move.
A robot should continuously check weather it is safe to move.

Emergency stop must have the highest priority because it represents immediate danger.

## Obstacle recovery logic

If the robot detects an obstacle:

- stop motors
- wait and scan again 
- continue if the obstacle is cleared
- choose an alternative route if available
- call operator if no safe route exits 

## Distance logic 

I learned that safe movement is not the same as task completion.

- Distance greater than 0 means robot is still moving 
- Distance equal to 0 means robot reached the destination
- Delivery count should increase only after successful delivery completion

## Robotics connection 

This connects to ROS2  because later these manual inputs can become real robot sensor data:
- emergency stop topic
- battery status topic
- obstacle detection topic
- navigation distance topic
- delivery status topic

## Reflection 

Today I understood that loops are very important in robotics. Robots keep checking sensors again and again while making decisions. I also learned that good robot logic needs saftey pirority, recovery behaviour, and clear mission completion.
