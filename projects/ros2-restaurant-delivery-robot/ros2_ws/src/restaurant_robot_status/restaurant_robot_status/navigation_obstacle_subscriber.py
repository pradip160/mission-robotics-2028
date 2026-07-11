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
 
        self.motor_command_publisher = self.create_publisher(
            String,
            'motor_command',
            10
        )

   
    def receive_obstacle(self, message):
        obstacle_status = message.data
        motor_command = String()

        if obstacle_status == 'OBSTACLE_DETECTED':
            self.get_logger().info('Obstacle detected — stopping and changing direction')
            motor_command.data = 'TURN_LEFT'

        elif obstacle_status == 'PATH_CLEAR':
            self.get_logger().info('Path clear — continuing navigation')
            motor_command.data = 'MOVE_FORWARD'
  
        elif obstacle_status == 'PERSON_DETECTED':
            self.get_logger().info('Person detected - stopping and waiting')
            motor_command.data = 'STOP_AND_WAIT'
            
        else:
            self.get_logger().warning(
                'Unknown obstacle status - stopping for safety'
            )
            motor_command.data = 'STOP'

        self.motor_command_publisher.publish(motor_command)
        self.get_logger().info(
            f'Motor command published: {motor_command.data}'
        )

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

