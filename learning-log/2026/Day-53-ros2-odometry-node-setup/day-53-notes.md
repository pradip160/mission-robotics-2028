# Day 53 – ROS2 Odometry Node Setup

**Date:** September 12, 2026  
**Mission:** Korea 2028  
**Topic:** First ROS2 odometry implementation

## Goal

Start applying odometry theory to the real ROS2 restaurant robot simulation.

Planned flow:

wheel joint angles  
→ wheel angle change  
→ wheel distance  
→ robot movement  
→ x, y, theta  
→ /odom  
→ TF odom → base_link

---

## 1. Created Odometry Node

Created:

`restaurant_robot_status/odometry_node.py`

Basic node:

```python
import rclpy
from rclpy.node import Node

class OdometryNode(Node):

    def __init__(self):
        super().__init__('odometry_node')
        self.get_logger().info('Odometry node started')


def main(args=None):
    rclpy.init(args=args)

    node = OdometryNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
2. Error Fixed

I first wrote:

from rclpy.node import node

This was wrong because Python is case-sensitive.

Correct version:

from rclpy.node import Node
3. Node Successfully Started

Command:

python3 odometry_node.py

Output:

[odometry_node]: Odometry node started

The terminal stayed active because:

rclpy.spin(node)

keeps the ROS2 node running.

4. Confirmed ROS2 Node

Command:

ros2 node list

Output:

/odometry_node

This confirms the first odometry node structure is working.

5. Planned Odometry Input

The odometry node eventually needs wheel joint information.

Expected ROS topic:

/joint_states

Message type:

sensor_msgs/msg/JointState

Important values:

left wheel angle
right wheel angle

Represented as:

$$ \phi_L $$

and:

$$ \phi_R $$

The change in wheel angle will be:

$$ \Delta\phi_L = \phi_{L,new}-\phi_{L,old} $$ $$ \Delta\phi_R = \phi_{R,new}-\phi_{R,old} $$

Then wheel distance:

$$ \Delta s_L=r\Delta\phi_L $$ $$ \Delta s_R=r\Delta\phi_R $$
6. Planned Odometry Output

The node will eventually publish:

/odom

using:

nav_msgs/msg/Odometry

It will contain:

Pose
$$ x,\ y,\ \theta $$
Velocity
$$ v,\ \omega $$

The node will also eventually publish the TF relationship:

odom → base_link
7. Simulation Files Found

Robot SDF:

~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_description/models/restaurant_robot.sdf

Robot URDF:

~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_description/urdf/restaurant_robot.urdf

World:

~/mission-korea/projects/ros2-restaurant-delivery-robot/ros2_ws/src/restaurant_robot_description/worlds/restaurant_world.sdf
8. Gazebo Topics Checked

Command:

gz topic -l | grep -Ei 'joint|wheel|lidar|scan'

Output:

/lidar
/lidar/points

This confirms the LiDAR is running in Gazebo.

However, wheel joint states are not currently being published.

9. ROS2 Topics Checked

Command:

ros2 topic list

Output:

/parameter_events
/rosout

There is currently no:

/joint_states

So the odometry node does not yet have wheel encoder-style input.

10. Wheel Joints Confirmed

The robot SDF contains:

left_wheel_joint
right_wheel_joint

Both are revolute joints.

The SDF also contains the Gazebo differential-drive plugin:

gz::sim::systems::DiffDrive

with:

<left_joint>left_wheel_joint</left_joint>
<right_joint>right_wheel_joint</right_joint>

So Gazebo already knows which wheels control the robot.

11. Current Problem

The robot wheels exist and move, but their joint angles are not currently exposed as joint-state data.

Current situation:

DiffDrive
   ↓
left and right wheels move
   ↓
no joint state topic
   ↓
no /joint_states
   ↓
odometry_node cannot read wheel angles yet
12. Next Step

Next session, add the Gazebo joint-state publisher plugin inside:

restaurant_robot.sdf

Planned plugin:

<plugin
  filename="gz-sim-joint-state-publisher-system"
  name="gz::sim::systems::JointStatePublisher">

  <joint_name>left_wheel_joint</joint_name>
  <joint_name>right_wheel_joint</joint_name>

</plugin>

Then completely restart Gazebo and respawn the robot.

After restart, check:

gz topic -l | grep joint

The goal is to see wheel joint-state information.

After that:

Gazebo joint states
→ ROS2 bridge
→ /joint_states
→ odometry_node

Then begin calculating:

$$ \Delta\phi_L,\Delta\phi_R $$

and later:

$$ x,y,\theta $$
Learning Evidence

Today I:

created my first ROS2 odometry node
fixed a Python Node import error
successfully ran /odometry_node
confirmed the node using ros2 node list
recovered my robot SDF, URDF and world files
confirmed LiDAR topics exist in Gazebo
confirmed left and right wheel joints exist
confirmed the DiffDrive plugin uses those wheel joints
discovered that wheel joint states are not currently being published
identified the missing layer needed before real odometry calculation
