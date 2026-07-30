import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32

class RearObstaclePublisher(Node):

    def __init__(self):
        super().__init__('rear_obstacle_publisher')
        self.publisher = self.create_publisher(
            String,
            'rear_status',
            10
        )
        self.distance_publisher = self.create_publisher(
             Float32,
            'rear_distance',
            10
        )

        self.obstacle_present = False

        self.timer = self.create_timer(
            1.0,
            self.publish_rear_status
        )

    def publish_rear_status(self):
        message = String()
        distance_message = Float32()
        if self.obstacle_present:
            message.data = 'OBSTACLE_DETECTED'
            distance_message.data = 0.6
        else:
            message.data = 'PATH_CLEAR'
            distance_message.data = 3.0
        self.publisher.publish(message)
        self.distance_publisher.publish(distance_message)
        self.get_logger().info(
            f'Rear_obstacle: {message.data}'
        )
        self.get_logger().info(
            f'Rear distance: {distance_message.data}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = RearObstaclePublisher()

    try:
        rclpy.spin(node)
 
    except KeyboardInterrupt:
        pass
    
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()

