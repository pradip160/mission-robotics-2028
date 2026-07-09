import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class NavigationObstacleSubscriber(Node):

    def __init__(self):
        super().__init__('navigation_obstacle_subscriber')
        self.subscription = self.create_subscription(
            String,
            'obstacle_status',
            self.receive_obstacle,
            10
        )
    
    def receive_obstacle(self, message):
        obstacle_status = message.data
        if obstacle_status == 'OBSTACLE_DETECTED':
            self.get_logger().info('Obstacle detected — changing direction')



def main(args=None):
    rclpy.init(args=args)
    node = NavigationObstacleSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()
