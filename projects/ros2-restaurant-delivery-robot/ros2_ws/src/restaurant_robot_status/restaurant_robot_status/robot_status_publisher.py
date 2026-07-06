import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class RobotStatusPublisher(Node):

    def __init__(self):
        super().__init__('robot_status_publisher')
        self.publisher_ = self.create_publisher(
            String,
            'robot_status',
            10
        )
        self.timer_ = self.create_timer(
            1.0,
            self.publish_status
        )
    def publish_status(self):
        message = String()
        message.data = 'SAFETY_CHECK'
        self.publisher_.publish(message)
        self.get_logger().info(
            f'Publishing robot status: {message.data}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = RobotStatusPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
