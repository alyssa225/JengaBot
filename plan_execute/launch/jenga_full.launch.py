"""
want to launch: 

ros2 launch franka_moveit_config rviz.launch.py robot_ip:=panda0.robot
ros2 run plan_execute cv_test
ros2 launch camera jenga_vision.launch.py 
ros2 run flask_ros flask

"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    launch_franka = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('franka_moveit_config'),
                    'launch/rviz.launch.py'
                ])
            ]),
        launch_arguments=[('robot_ip', 'panda0.robot')]
    )

    movement_node = Node(
        package='plan_execute',
        executable='cv_test',
        output='screen'
    )

    launch_vision = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('camera'),
                    'jenga_vision.launch.py'
                ])
            ]),
        launch_arguments=[('robot_ip', 'panda0.robot')]
    )

    flask_node = Node(
        package='flask_ros',
        executable='flask',
        output='screen'
    )

    return LaunchDescription([
        launch_franka,
        movement_node,
        launch_vision,
        flask_node
    ])
