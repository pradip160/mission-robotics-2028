import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSProfile,
    ReliabilityPolicy,
    HistoryPolicy,
    DurabilityPolicy
)
from std_msgs.msg import String, Float32

class LidarObstaclePublisher(Node):

    def __init__(self):
        super().__init__('lidar_obstacle_publisher')
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
            durability=DurabilityPolicy.VOLATILE
        )
        self.publisher = self.create_publisher(
            String,
            'lidar_status',
            10
        )
        self.distance_publisher = self.create_publisher(
             Float32,
            'lidar_distance',
            sensor_qos
        )

        self.obstacle_present = False

        self.timer = self.create_timer(
            1.0,
            self.publish_lidar_status
        )

    def publish_lidar_status(self):
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
        self.obstacle_present = not self.obstacle_present
        self.get_logger().info(
            f'Lidar_obstacle: {message.data}'
        )
        self.get_logger().info(
            f'lidar distance: {distance_message.data}'
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
