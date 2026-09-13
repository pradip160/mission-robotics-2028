import rclpy
import math 
from rclpy.node import Node 
from sensor_msgs.msg import JointState 

class OdometryNode(Node):

    def __init__(self):
        super().__init__('odometry_node')
        
        self.get_logger().info('Odometry node started')

        self.wheel_radius = 0.10
        self.wheel_separation = 0.60

        self.previous_left_angle = None
        self.previous_right_angle = None


        self.joint_state_subscriber = self.create_subscription(
            JointState,
            '/world/restaurant_world/model/restaurant_robot/joint_state',
            self.joint_state_callback,
            10
        )

    def joint_state_callback(self, msg):
        left_index = msg.name.index('left_wheel_joint')
        right_index = msg.name.index('right_wheel_joint')

        left_angle = msg.position[left_index]
        right_angle = msg.position[right_index]

        if self.previous_left_angle is None:
            self.previous_left_angle = left_angle
            self.previous_right_angle = right_angle
            return

        delta_left_angle = left_angle - self.previous_left_angle
        delta_right_angle = right_angle - self.previous_right_angle

        delta_left_distance = self.wheel_radius * delta_left_angle
        delta_right_distance = self.wheel_radius * delta_right_angle

        delta_s = (delta_right_distance + delta_left_distance) /2.0

        delta_theta = (
            delta_right_distance - delta_left_distance
        ) / self.wheel_separation


        self.previous_left_angle = left_angle
        self.previous_right_angle = right_angle

        self.get_logger().info(
            f'delta_s: {delta_s:.6f} m | '
            f'delta_theta: {delta_theta:.6f} rad'
        )
def main(args=None):
    rclpy.init(args=args)

    node = OdometryNode()
    
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
