import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    config_file = os.path.join(
        get_package_share_directory('restaurant_robot_status'),
        'config',
        'navigation_params.yaml'
    )
    sensor_timeout = LaunchConfiguration('sensor_timeout')

    sensor_timeout_value = ParameterValue(
        sensor_timeout,
        value_type=float
    )

    return LaunchDescription([

    DeclareLaunchArgument(
        'sensor_timeout',
        default_value='4.0',
        description='Maximum sensor message age before it becomes stale'
    ),

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
            executable='rear_obstacle_publisher',
            output='screen'
        ),
        Node(
            package='restaurant_robot_status',
            executable='navigation_obstacle_subscriber',
            parameters=[
                config_file,
                {'sensor_timeout': sensor_timeout_value}
            ],
            output='screen'
        ),
        Node(
            package='restaurant_robot_status',
            executable='motor_control_subscriber',
            output='screen'
        )
    ])
  

