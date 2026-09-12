import rclpy
from rclpy.node import Node 


class OdometryNode(Node):

    def __init__(self):
        super().__init__('odometry_node')
        
        self.get_logger().info('Odometry node started')



def main(args=None):
    rclpy.init(args=args)

    node = OdometryNode()
    
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
