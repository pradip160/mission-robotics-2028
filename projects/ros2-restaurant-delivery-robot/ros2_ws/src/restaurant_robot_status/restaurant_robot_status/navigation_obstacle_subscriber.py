import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class NavigationObstacleSubscriber(Node):

    def __init__(self):
        super().__init__('navigation_obstacle_subscriber')
        self.camera_state = 'UNKNOWN'
        self.lidar_state = 'UNKNOWN'
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

        self.lidar_subscription = self.create_subscription(
            String,  
            'lidar_status',
            self.receive_lidar,
            10
        )
  

   


    def receive_obstacle(self, message):
        self.camera_state = message.data
        self.decide_navigation()



    def receive_lidar(self, message):
        self.lidar_state = message.data 
        self.decide_navigation()

    def decide_navigation(self):
        motor_command = String()
        if self.camera_state == 'UNKNOWN' or self.lidar_state == 'UNKNOWN':
             motor_command.data = 'STOP'

        elif self.camera_state == 'OBSTACLE_DETECTED' or self.lidar_state == 'OBSTACLE_DETECTED':
             motor_command.data = 'STOP'
      
        elif self.camera_state == 'PATH_CLEAR' and self.lidar_state == 'PATH_CLEAR':
             motor_command.data = 'MOVE_FORWARD' 
        
        else: 
             motor_command.data = 'STOP'
        
        self.motor_command_publisher.publish(motor_command)
        self.get_logger().info(
             f'Camera: {self.camera_state}, LiDAR: {self.lidar_state}, Command: {motor_command.data}'
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

