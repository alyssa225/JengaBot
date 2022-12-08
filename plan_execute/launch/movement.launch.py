from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_path


def generate_launch_description():

    plan_execute_path = get_package_share_path('plan_execute')
    turns_yaml = plan_execute_path / 'turns.yaml'

    movement_node = Node(
        package='plan_execute',
        executable='cv_test',
        output='screen',
        parameters=[turns_yaml],
    )

    # ros2 launch franka_moveit_config rviz.launch.py robot_ip:=panda0.robot
    launch_franka = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('franka_moveit_config'),
                    'launch/rviz.launch.py'
                ])
            ]),
        launch_arguments=[('robot_ip', 'panda0.robot')]
    )

    return LaunchDescription([
        launch_franka,
        movement_node
    ])
