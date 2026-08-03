import rclpy
from rclpy.node import Node 
from rclpy.qos import QoSProfile 
from rclpy.qos import ReliabilityPolicy
from rclpy.qos import HistoryPolicy
from rclpy.qos import DurabilityPolicy

from std_msgs.msg import Int32

class QoSDepthTestPublisher(Node):

    def __init__(self):
        super().__init__('qos_depth_test_publisher')

        depth_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
            durability=DurabilityPolicy.VOLATILE
        )
        self.number = 0


        self.publisher = self.create_publisher(
            Int32,
            '/qos_depth_test',
            depth_qos,
        )

        self.timer = self.create_timer(
            0.01,
            self.publish_number
        )

    def publish_number(self):
        self.number += 1

        msg = Int32()
        msg.data = self.number

        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    node = QoSDepthTestPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
