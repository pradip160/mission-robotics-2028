import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class RobotReadinessClient(Node):
    def __init__(self):
        super().__init__('robot_readiness_client')

        self.client = self.create_client(
            Trigger,
            'check_robot_ready'
        )

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'Waiting for /check_robot_ready service...'
            )

    def send_request(self):
        request = Trigger.Request()
        future = self.client.call_async(request)
        return future
 
def main(args=None):
    rclpy.init(args=args)
    node = None 

    try:
        node = RobotReadinessClient()
        future = node.send_request()

        rclpy.spin_until_future_complete(node, future)
    
        response = future.result()

        node.get_logger().info(
            f'Robot ready: {response.success} | Reason: {response.message}'
        )
    except KeyboardInterrupt:
        pass
    except Exception as error:
        if node is not None:
            node.get_logger().error(
                f'Service call failed: {error}'
            )
        else:
            print(f'Service call failed: {error}')
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
