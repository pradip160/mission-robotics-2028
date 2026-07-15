import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class NavigationObstacleSubscriber(Node):

    def __init__(self):
        super().__init__('navigation_obstacle_subscriber')
        self.sensor_timeout = 3.0
        self.front_state = 'UNKNOWN'

        self.left_state = 'UNKNOWN'
        self.last_left_message_time = None
        self.left_fresh = False 
 
        self.right_state = 'UNKNOWN'
        self.last_right_message_time = None 
        self.right_fresh = False

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
        self.left_subscription = self.create_subscription(
            String,
            'left_status',
            self.receive_left,
            10
        )
        self.right_subscription = self.create_subscription(
            String,
            'right_status',
            self.receive_right,
            10
        )
  

        self.safety_timer = self.create_timer(
            1.0,
            self.check_sensor_freshness
        )    


    def receive_obstacle(self, message):
        self.camera_state = message.data
        self.last_camera_message_time = self.get_clock().now()
        self.decide_navigation()



    def receive_lidar(self, message):
        self.lidar_state = message.data 
        self.last_lidar_message_time = self.get_clock().now()
        self.decide_navigation()

    def receive_left(self, message):
        self.left_state = message.data 
        self.last_left_message_time = self.get_clock().now()
        self.decide_navigation()

    def receive_right(self, message):
        self.right_state = message.data
        self.last_right_message_time = self.get_clock().now()
        self.decide_navigation()

    def decide_navigation(self):
        self.update_front_state()
        motor_command = String()

        if not self.camera_fresh or not self.lidar_fresh:
             motor_command.data = 'STOP'

        elif self.front_state == 'UNKNOWN':
             motor_command.data = 'STOP'

        elif self.front_state == 'OBSTACLE_DETECTED':
             if self.left_fresh and self.left_state == 'PATH_CLEAR':
                  motor_command.data = 'TURN_LEFT'

             elif self.right_fresh and self.right_state == 'PATH_CLEAR':
                  motor_command.data = 'TURN_RIGHT'

             else:
                  motor_command.data = 'STOP' 

      
        elif self.front_state == 'PATH_CLEAR':
             motor_command.data = 'MOVE_FORWARD'        
        else: 
             motor_command.data = 'STOP'
        
        self.motor_command_publisher.publish(motor_command)
        self.get_logger().info(
             f'Camera: {self.camera_state}, LiDAR: {self.lidar_state}, Front: {self.front_state}, Left: {self.left_state},  Left fresh: {self.left_fresh}, Right: {self.right_state}, Right fresh: {self.right_fresh}, Command: {motor_command.data}'
        )

    def check_sensor_freshness(self):
        current_time = self.get_clock().now()

        if self.last_camera_message_time is None or self.last_lidar_message_time is None:
            self.camera_fresh = False
            self.lidar_fresh = False
            self.decide_navigation()
            return

        if self.last_left_message_time is None:
            self.left_fresh = False 
        else:
            left_age = current_time - self.last_left_message_time
            left_age_seconds = left_age.nanoseconds / 1_000_000_000
            self.left_fresh = left_age_seconds <= self.sensor_timeout
 
        if self.last_right_message_time is None:
            self.right_fresh = False
        else:
            right_age = current_time - self.last_right_message_time
            right_age_seconds = right_age.nanoseconds / 1_000_000_000
            self.right_fresh = right_age_seconds <= self.sensor_timeout


        camera_age = current_time - self.last_camera_message_time
        lidar_age = current_time - self.last_lidar_message_time

        camera_age_seconds = camera_age.nanoseconds / 1_000_000_000
        lidar_age_seconds = lidar_age.nanoseconds / 1_000_000_000

        self.camera_fresh = camera_age_seconds <= self.sensor_timeout
        self.lidar_fresh = lidar_age_seconds <= self.sensor_timeout

        self.decide_navigation()


    def update_front_state(self):
        if self.camera_state == 'OBSTACLE_DETECTED' or self.lidar_state == 'OBSTACLE_DETECTED':
            self.front_state = 'OBSTACLE_DETECTED'

        elif self.camera_state == 'PATH_CLEAR' and self.lidar_state == 'PATH_CLEAR': 
            self.front_state = 'PATH_CLEAR'

        else: 
            self.front_state = 'UNKNOWN'

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

