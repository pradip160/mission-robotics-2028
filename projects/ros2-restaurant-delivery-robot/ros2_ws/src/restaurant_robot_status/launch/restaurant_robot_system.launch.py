from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='restaurant_robot_status',
            executable='camera_obstacle_publisher',
            output='screen'
        ),
        Node(
            package='restaurant_robot_status',
            executable='lidar_obstacle_publisher',
            output='screen'
        ),
        Node(
            package='restaurant_robot_status',
            executable='left_obstacle_publisher',
            output='screen'
        ),
        Node(
            package='restaurant_robot_status',
            executable='right_obstacle_publisher',
            output='screen'
        ),
        Node(
            package='restaurant_robot_status',
            executable='navigation_obstacle_subscriber',
            output='screen'
        ),
        Node(
            package='restaurant_robot_status',
            executable='motor_control_subscriber',
            output='screen'
        )
    ])
  

