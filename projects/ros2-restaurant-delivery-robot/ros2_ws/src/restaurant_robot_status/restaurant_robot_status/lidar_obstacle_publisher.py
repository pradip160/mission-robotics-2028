import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSProfile,
    ReliabilityPolicy,
    HistoryPolicy,
    DurabilityPolicy
)
from restaurant_robot_interfaces.msg import LidarObservation

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
            LidarObservation,
            '/lidar_observation',
            sensor_qos
        )

        self.obstacle_present = False

        self.timer = self.create_timer(
            1.0,
            self.publish_lidar_observation
        )

    def publish_lidar_observation(self):
        message = LidarObservation()

        if self.obstacle_present:
            message.status = 'OBSTACLE_DETECTED'
            message.distance = 0.6
        else:
            message.status = 'PATH_CLEAR'
            message.distance = 3.0

        message.valid = True

        self.publisher.publish(message)

        self.get_logger().info(
            f'LiDAR observation: status={message.status}, '
            f'distance={message.distance:.2f} m, '
            f'valid={message.valid}'
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
