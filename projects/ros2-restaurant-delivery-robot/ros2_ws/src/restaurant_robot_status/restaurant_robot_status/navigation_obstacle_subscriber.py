import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class NavigationObstacleSubscriber(Node):

    def __init__(self):
        super().__init__('navigation_obstacle_subscriber')
        self.sensor_timeout = 3.0
        self.camera_state = 'UNKNOWN'
        self.last_camera_message_time = None
        self.camera_fresh = False

        self.lidar_state = 'UNKNOWN'
        self.last_lidar_message_time = None 
        self.lidar_fresh = False

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
  

        self.saftey_timer = self.create_timer(
            1.0,
            self.check_sensor_freshness
        )    


    def receive_obstacle(self, message):
        self.camera_state = message.data
        self.decide_navigation()



    def receive_lidar(self, message):
        self.lidar_state = message.data 
        self.decide_navigation()

    def decide_navigation(self):
        motor_command = String()

        if not self.camera_fresh or not self.lidar_fresh:
             motor_command.data = 'STOP'

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

    def check_sensor_freshness(self):
        current_time = self.get_clock().now()

        if self.last_camera_message_time is None or self.last_lidar_message_time is None:
            self.camera_fresh = False
            self.lidar_fresh = False
            self.decide_navigation()
            return
        
        camera_age = current_time - self.last_camera_message_time
        lidar_age = current_time - self.last_lidar_message_time

        camera_age_seconds = camera_age.nanoseconds / 1_000_000_000
        lidar_age_seconds = lidar_age.nanoseconds / 1_000_000_000

        self.camera_fresh = camera_age_seconds <= self.sensor_timeout
        self.lidar_fresh = lidar_age_seconds <= self.sensor_timeout

        self.decide_navigation()

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

