import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class MotorControlSubscriber(Node):
    def __init__(self):
        super().__init__('motor_control_subscriber')
        self.subscription = self.create_subscription(
            String,
            'motor_command',
            self.receive_motor_command,
            10
        )

        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

    def receive_motor_command(self, message):
        motor_command = message.data
        cmd_vel =Twist() 
        if motor_command == 'MOVE_FORWARD':
            cmd_vel.linear.x = 0.2
            cmd_vel.angular.z = 0.0

            self.cmd_vel_publisher.publish(cmd_vel)

            self.get_logger().info(
                'Both wheels moving forward at the same speed'
            )
        elif motor_command == 'TURN_LEFT':
            cmd_vel.linear.x = 0.1
            cmd_vel.angular.z = 0.5

            self.cmd_vel_publisher.publish(cmd_vel)
            self.get_logger().info(
                'Left wheel slowing down and right wheel moving faster'
            )
        elif motor_command == 'TURN_RIGHT':
            cmd_vel.linear.x = 0.1
            cmd_vel.angular.z = -0.5

            self.cmd_vel_publisher.publish(cmd_vel)

            self.get_logger().info(
                'Right wheel slowing down and left wheel moving faster'
            )
        elif motor_command == 'MOVE_BACKWARD':
            cmd_vel.linear.x = -0.2
            cmd_vel.angular.z = 0.0

            self.cmd_vel_publisher.publish(cmd_vel)

            self.get_logger().info(
                'Both wheels move backward'
            )
        elif motor_command == 'STOP_AND_WAIT':
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = 0.0
            self.cmd_vel_publisher.publish(cmd_vel)
            self.get_logger().info(
                'Both wheels stop and wait'
            )
        elif motor_command == 'STOP':
            cmd_vel.linear.x = 0.0 
            cmd_vel.angular.z = 0.0
            self.cmd_vel_publisher.publish(cmd_vel)
            self.get_logger().info(
                'Both wheels stop safely'
            )
        else:
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = 0.0 
            self.cmd_vel_publisher.publish(cmd_vel)
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
