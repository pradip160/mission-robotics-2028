import rclpy
import math 

from rclpy.node import Node 
from sensor_msgs.msg import JointState 
from nav_msgs.msg import Odometry
from geometry_msgs.msg  import TransformStamped
from tf2_ros import TransformBroadcaster

class OdometryNode(Node):

    def __init__(self):
        super().__init__('odometry_node')
        
        self.get_logger().info('Odometry node started')

        self.wheel_radius = 0.10
        self.wheel_separation = 0.60

        self.x = 0.0
        self.y = 0.0 
        self.theta = 0.00


        self.previous_left_angle = None
        self.previous_right_angle = None
        self.previous_time = None


        self.joint_state_subscriber = self.create_subscription(
            JointState,
            '/world/restaurant_world/model/restaurant_robot/joint_state',
            self.joint_state_callback,
            10
        )
        self.odom_publisher = self.create_publisher(
            Odometry,
            '/odom',
            10
        )
        self.tf_broadcaster = TransformBroadcaster(self)

    def joint_state_callback(self, msg):
        left_index = msg.name.index('left_wheel_joint')
        right_index = msg.name.index('right_wheel_joint')

        left_angle = msg.position[left_index]
        right_angle = msg.position[right_index]

        current_time = (
            msg.header.stamp.sec +
            msg.header.stamp.nanosec * 1e-9
        )

        if self.previous_left_angle is None:
            self.previous_left_angle = left_angle
            self.previous_right_angle = right_angle
            self.previous_time = current_time 
            return

        delta_left_angle = left_angle - self.previous_left_angle
        delta_right_angle = right_angle - self.previous_right_angle

        delta_left_distance = self.wheel_radius * delta_left_angle
        delta_right_distance = self.wheel_radius * delta_right_angle

        delta_s = (delta_right_distance + delta_left_distance) /2.0

        delta_theta = (
            delta_right_distance - delta_left_distance
        ) / self.wheel_separation

        delta_t = current_time - self.previous_time

        if delta_t <= 0.0:
            return 

        linear_velocity = delta_s / delta_t
        angular_velocity = delta_theta /delta_t

        theta_mid = self.theta + delta_theta / 2.0

        delta_x = delta_s * math.cos(theta_mid)
        delta_y = delta_s * math.sin(theta_mid)

        self.x += delta_x
        self.y += delta_y
        self.theta += delta_theta

        odom_msg = Odometry()

        odom_msg.header.stamp = msg.header.stamp
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'

        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0

        odom_msg.pose.pose.orientation.x = 0.0
        odom_msg.pose.pose.orientation.y = 0.0
        odom_msg.pose.pose.orientation.z = math.sin(self.theta / 2.0)
        odom_msg.pose.pose.orientation.w = math.cos(self.theta / 2.0)

        odom_msg.twist.twist.linear.x = linear_velocity
        odom_msg.twist.twist.angular.z = angular_velocity

        self.odom_publisher.publish(odom_msg)

        transform_msg = TransformStamped()

        transform_msg.header.stamp = msg.header.stamp
        transform_msg.header.frame_id = 'odom'
        transform_msg.child_frame_id = 'base_link'

        transform_msg.transform.translation.x = self.x 
        transform_msg.transform.translation.y = self.y 
        transform_msg.transform.translation.z = 0.0

        transform_msg.transform.rotation.x = 0.0 
        transform_msg.transform.rotation.y = 0.0 
        transform_msg.transform.rotation.z = math.sin(self.theta / 2.0)
        transform_msg.transform.rotation.w = math.cos(self.theta / 2.0)

        self.tf_broadcaster.sendTransform(transform_msg)

        self.previous_left_angle = left_angle
        self.previous_right_angle = right_angle
        self.previous_time = current_time 

        self.get_logger().info(
            f'Pose -> x: {self.x:.4f} m | '
            f'y: {self.y:.4f} m |'
            f'theta: {self.theta:.4f} rad'
            f'theta: {self.theta:.4f} rad | ' 
            f'v: {linear_velocity:.4f} m/s | '
            f'omega: {angular_velocity:.4f} rad/s '  
        )

def main(args=None):
    rclpy.init(args=args)

    node = OdometryNode()
    
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


