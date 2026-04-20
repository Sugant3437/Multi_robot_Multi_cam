from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():

    map_file = os.path.join(
        os.getenv('HOME'),
        'ros2_ws/src/amr_nav/maps/map.yaml'
    )

    return LaunchDescription([

        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            parameters=[{'yaml_filename': map_file}],
            output='screen'
        ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager',
            parameters=[{
                'autostart': True,
                'node_names': ['map_server']
            }]
        ),

        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen'
        ),
    ])