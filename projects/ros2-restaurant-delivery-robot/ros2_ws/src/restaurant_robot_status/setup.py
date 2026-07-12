from setuptools import find_packages, setup

package_name = 'restaurant_robot_status'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pradip',
    maintainer_email='pradipmainai5@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'robot_status_publisher = restaurant_robot_status.robot_status_publisher:main',
            'robot_status_subscriber = restaurant_robot_status.robot_status_subscriber:main',
            'camera_obstacle_publisher = restaurant_robot_status.camera_obstacle_publisher:main',
            'navigation_obstacle_subscriber = restaurant_robot_status.navigation_obstacle_subscriber:main',
            'motor_control_subscriber = restaurant_robot_status.motor_control_subscriber:main',
            'lidar_obstacle_publisher = restaurant_robot_status.lidar_obstacle_publisher:main',
 
       ]
    },	
)
	
