import math
import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSProfile,
    ReliabilityPolicy,
    HistoryPolicy,
    DurabilityPolicy
)
from std_msgs.msg import String, Float32
from rcl_interfaces.msg import SetParametersResult

class NavigationObstacleSubscriber(Node):
    def __init__(self):
        super().__init__('navigation_obstacle_subscriber')
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
            durability=DurabilityPolicy.VOLATILE
        )
        self.declare_parameter('sensor_timeout', 3.0)
        self.sensor_timeout = self.get_parameter('sensor_timeout').value
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.front_state = 'UNKNOWN'
        self.recovery_state = 'NORMAL'
        self.recovery_clear_distance = 1.5
        self.recovery_start_time = None
        self.maximum_recovery_duration = 5.0

        self.recovery_start_time = 'REVERSING' 
        

        self.left_state = 'UNKNOWN'
        self.last_left_message_time = None
        self.left_fresh = False
        self.previous_left_fresh = None

        self.right_state = 'UNKNOWN'
        self.last_right_message_time = None
        self.right_fresh = False
        self.previous_right_fresh = None

        self.camera_state = 'UNKNOWN'
        self.last_camera_message_time = None
        self.camera_fresh = False
        self.previous_camera_fresh = None

        self.lidar_state = 'UNKNOWN'
        self.last_lidar_message_time = None
        self.lidar_fresh = False
        self.previous_lidar_fresh = None

        self.lidar_distance = 0.0
        self.last_lidar_distance_message_time = None
        self.lidar_distance_fresh = False

        self.rear_state = 'UNKNOWN'
        self.last_rear_message_time = None
        self.rear_fresh = False
        self.previous_rear_fresh = None

        self.rear_distance = 0.0
        self.last_rear_distance_message_time = None
        self.rear_distance_fresh = False

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
        self.lidar_distance_subscription = self.create_subscription(
            Float32,
            'lidar_distance',
            self.receive_lidar_distance,
            sensor_qos
        )
        self.rear_subscription = self.create_subscription(
            String,
            'rear_status',
            self.receive_rear,
            10
        )
        self.rear_distance_subscription = self.create_subscription(
            Float32,
            'rear_distance',
            self.receive_rear_distance,
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


    def parameter_callback(self, parameters):
        for parameter in parameters:
            if parameter.name == 'sensor_timeout':
                if parameter.value <= 0.0:
                    return SetParametersResult(
                        successful=False,
                        reason='sensor_timeout must be greater than 0.0'
                    )

                self.sensor_timeout = parameter.value
                self.get_logger().info(
                    f'Sensor timeout updated to: {self.sensor_timeout} seconds'
                    )


        return SetParametersResult(successful=True)

    def receive_obstacle(self, message):
        self.camera_state = message.data
        self.last_camera_message_time = self.get_clock().now()
        self.decide_navigation()



    def receive_lidar(self, message):
        self.lidar_state = message.data
        self.last_lidar_message_time = self.get_clock().now()
        self.decide_navigation()

    def receive_lidar_distance(self, message):
        self.lidar_distance = message.data
        self.last_lidar_distance_message_time = self.get_clock().now()
        self.decide_navigation()

    def receive_rear(self, message):
        self.rear_state = message.data
        self.last_rear_message_time = self.get_clock().now()
        self.decide_navigation()

    def receive_rear_distance(self, message):
        self.rear_distance = message.data
        self.last_rear_distance_message_time = self.get_clock().now()
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

        if (
            not self.camera_fresh
            or not self.lidar_fresh
            or not self.lidar_distance_fresh
            or not self.rear_fresh
            or not self.rear_distance_fresh
            or not self.left_fresh
            or not self.right_fresh
        ):
            motor_command.data = 'STOP'
        elif (
            not math.isfinite(self.lidar_distance)
            or self.lidar_distance <= 0.0
            or not math.isfinite(self.rear_distance)
            or self.rear_distance <= 0.0
        ):
            motor_command.data = 'STOP'
        elif (
            self.front_state == 'UNKNOWN'
            or self.left_state == "UNKNOWN"
            or self.right_state == "UNKNOWN"
            or self.rear_state == 'UNKNOWN'
        ):
            motor_command.data = 'STOP'
      

        elif self.recovery_state == 'RECOVERY_FAILED':
            motor_command.data = 'STOP_AND_WAIT'


        elif self.recovery_state == 'REVERSING':
            current_time = self.get_clock().now()
            recovery_elapsed = current_time - self.recovery_start_time
            recovery_elapsed_seconds = recovery_elapsed.nanoseconds / 1_000_000_000

            if recovery_elapsed_seconds >= self.maximum_recovery_duration:
                self.recovery_state = 'RECOVERY_FAILED'
                motor_command.data = 'STOP_AND_WAIT'

            elif (
                self.rear_state != 'PATH_CLEAR'
                or self.rear_distance <= 1.0
            ):
                motor_command.data = 'STOP'


            elif self.lidar_distance >= self.recovery_clear_distance:
                self.recovery_state = 'NORMAL'
                self.recovery_start_time = None
                motor_command.data = 'STOP'

            else:
                motor_command.data = 'MOVE_BACKWARD'


        elif self.lidar_distance <= 1.0:
            if (
                self.rear_state == 'PATH_CLEAR'
                and self.rear_distance > 1.0
            ):

                self.recovery_state = 'REVERSING'
                self.recovery_start_time = self.get_clock().now()
                motor_command.data = 'MOVE_BACKWARD'


            else:
                motor_command.data  = 'STOP'

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

        if self.last_camera_message_time is None:
            self.camera_fresh = False

        else:
            camera_age = current_time - self.last_camera_message_time
            camera_age_seconds = camera_age.nanoseconds / 1_000_000_000
            self.camera_fresh = camera_age_seconds <= self.sensor_timeout

        if self.last_lidar_message_time is None:
            self.lidar_fresh = False

        else:
            lidar_age = current_time - self.last_lidar_message_time
            lidar_age_seconds = lidar_age.nanoseconds / 1_000_000_000
            self.lidar_fresh = lidar_age_seconds <= self.sensor_timeout


        if self.last_lidar_distance_message_time is None:
            self.lidar_distance_fresh = False

        else:
            lidar_distance_age = current_time - self.last_lidar_distance_message_time
            lidar_distance_age_seconds = lidar_distance_age.nanoseconds / 1_000_000_000
            self.lidar_distance_fresh = lidar_distance_age_seconds <= self.sensor_timeout



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

        if self.last_rear_message_time is None:
            self.rear_fresh = False
        else:
            rear_age = current_time - self.last_rear_message_time
            rear_age_seconds = rear_age.nanoseconds / 1_000_000_000
            self.rear_fresh = rear_age_seconds <= self.sensor_timeout

        if self.last_rear_distance_message_time is None:
            self.rear_distance_fresh = False
        else:
            rear_distance_age = current_time - self.last_rear_distance_message_time
            rear_distance_age_seconds  = rear_distance_age.nanoseconds / 1_000_000_000
            self.rear_distance_fresh = rear_distance_age_seconds <= self.sensor_timeout

        if self.previous_camera_fresh is True and self.camera_fresh is False:
            self.get_logger().warning(
                f'Camera became stale - age: {camera_age_seconds:.2f}s,'
                f'timeout: {self.sensor_timeout:.2f}s'
            )
        self.previous_camera_fresh = self.camera_fresh


        if self.previous_lidar_fresh is True and self.lidar_fresh is False:
            self.get_logger().warning(
                f'lidar became stale - age: {lidar_age_seconds:.2f}s,'
                f'timeout: {self.sensor_timeout:.2f}s'
            )
        self.previous_lidar_fresh = self.lidar_fresh

        if self.previous_left_fresh is True and self.left_fresh is False:
            self.get_logger().warning(
                f'Left became stale - age: {left_age_seconds:.2f}s,'
                f'timeout: {self.sensor_timeout:.2f}s'
            )
        self.previous_left_fresh = self.left_fresh

        if self.previous_right_fresh is True and self.right_fresh is False:
            self.get_logger().warning(
                f'Right became stale - age: {right_age_seconds:.2f}s,'
                f'timeout: {self.sensor_timeout:.2f}s'
            )
        self.previous_right_fresh = self.right_fresh


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
        rclpy.try_shutdown()



if __name__ == '__main__':
    main()

