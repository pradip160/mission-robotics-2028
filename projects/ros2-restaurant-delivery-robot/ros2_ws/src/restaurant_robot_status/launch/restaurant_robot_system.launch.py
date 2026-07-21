import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    config_file = os.path.join(
        get_package_share_directory('restaurant_robot_status'),
        'config',
        'navigation_params.yaml'
    )
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
            parameters=[config_file],
            output='screen'
        ),
        Node(
            package='restaurant_robot_status',
            executable='motor_control_subscriber',
            output='screen'
        )
    ])
  

