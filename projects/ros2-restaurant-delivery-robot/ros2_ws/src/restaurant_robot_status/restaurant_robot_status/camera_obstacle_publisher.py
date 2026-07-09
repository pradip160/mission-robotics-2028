import rclpy
from rclpy.node import Node 
from std_msgs.msg import String 


class CameraObstaclePublisher(Node):
     
     def __init__(self):
         super().__init__('camera_obstacle_publisher')
         self.publisher = self.create_publisher(
             String,
             'obstacle_status',
             10
         )
          
         self.timer = self.create_timer(
            1.0,
            self.publish_obstacle
        )

     def publish_obstacle(self):
         message = String()
         message.data = 'OBSTACLE_DETECTED'
         self.publisher.publish(message)
         self.get_logger().info(
             f'Camera detected: {message.data}'
         )


def main(args=None):
    rclpy.init(args=args)
    node = CameraObstaclePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

