import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MotorControlSubscriber(Node):
    def __init__(self):
        super().__init__('motor_control_subscriber')
        self.subscription = self.create_subscription(
            String,
            'motor_command',
            self.receive_motor_command,
            10
        )

    def receive_motor_command(self, message):
        motor_command = message.data
        if motor_command == 'MOVE_FORWARD':
            self.get_logger().info(
                'Both wheels moving forward at the same speed'
            )
        elif motor_command == 'TURN_LEFT':
            self.get_logger().info(
                'Left wheel slowing down and right wheel moving faster'
            )
        elif motor_command == 'TURN_RIGHT':
            self.get_logger().info(
                'Right wheel slowing down and left wheel moving faster'
            )
        elif motor_command == 'MOVE_BACKWARD':
            self.get_logger().info(
                'Both wheels move backward'
            )
        elif motor_command == 'STOP_AND_WAIT':
            self.get_logger().info(
                'Both wheels stop and wait'
            )
        elif motor_command == 'STOP':
            self.get_logger().info(
                'Both wheels stop safely'
            )
        else:
            self.get_logger().warning(
                'Unknown motor command - stopping safely'
            )

def main(args=None):
    rclpy.init(args=args)
    node = MotorControlSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()



if __name__ == '__main__':
    main()
