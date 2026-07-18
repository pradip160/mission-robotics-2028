import rclpy
from rclpy.node import Node 
from std_msgs.msg import String

class RightObstaclePublisher(Node):
    def __init__(self):
        super().__init__('right_obstacle_publisher')
        self.publisher = self.create_publisher(
            String,
            '/right_status',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_right_status
        )

    def publish_right_status(self):
        message = String()
        message.data = 'PATH_CLEAR'
        self.publisher.publish(message)
        self.get_logger().info(
            f'right_status: {message.data}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = RightObstaclePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
