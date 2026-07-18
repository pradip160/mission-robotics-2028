import rclpy
from rclpy.node import Node
from std_msgs.msg import String 

class LeftObstaclePublisher(Node):
    def __init__(self):
        super().__init__('left_obstacle_publisher')
        self.publisher = self.create_publisher(
            String,
            '/left_status',
            10
        )
        self.timer = self.create_timer(
            1.0,
            self.publish_left_status
        )

    def publish_left_status(self):
        message = String()
        message.data = 'PATH_CLEAR'
        self.publisher.publish(message)
        self.get_logger().info(
            f'left status: {message.data}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = LeftObstaclePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
