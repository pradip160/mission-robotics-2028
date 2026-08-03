import time 

import rclpy
from rclpy.node import Node 
from rclpy.qos import QoSProfile 
from rclpy.qos import ReliabilityPolicy
from rclpy.qos import HistoryPolicy 
from rclpy.qos import DurabilityPolicy

from std_msgs.msg import Int32


class QoSDepthTestSubscriber(Node):
 
    def __init__(self):
        super().__init__('qos_depth_test_subscriber')

        depth_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
            durability=DurabilityPolicy.VOLATILE
        )

        self.subscription = self.create_subscription(
            Int32,
            '/qos_depth_test',
            self.receive_number,
            depth_qos
        )

    def receive_number(self, msg):
        self.get_logger().info(f'Received number: {msg.data}')
        time.sleep(1.0)

def main(args=None):
    rclpy.init(args=args)

    node = QoSDepthTestSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
