import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class LidarObstaclePublisher(Node):

    def __init__(self):
        super().__init__('lidar_obstacle_publisher')
        self.publisher = self.create_publisher(
            String,
            'lidar_status',
            10
        )
        self.obstacle_present = False

        self.timer = self.create_timer(
            1.0,
            self.publish_lidar_status
        )

    def publish_lidar_status(self):
        message = String()
        if self.obstacle_present:
            message.data = 'OBSTACLE_DETECTED'
        else:
            message.data = 'PATH_CLEAR'
        self.publisher.publish(message)
        self.obstacle_present = not self.obstacle_present
        self.get_logger().info(
            f'Lidar_obstacle: {message.data}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = LidarObstaclePublisher()

    try:
        rclpy.spin(node)
 
    except KeyboardInterrupt:
        pass
    
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
