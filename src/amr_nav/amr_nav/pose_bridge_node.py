#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from amr_interfaces.msg import RobotPose

from geometry_msgs.msg import PoseWithCovarianceStamped
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

import math

class PoseBridge(Node):

    def __init__(self):
        super().__init__('pose_bridge')

        self.sub = self.create_subscription(
            RobotPose,
            '/robot_pose_cam',
            self.callback,
            10
        )

        self.pub = self.create_publisher(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            10
        )

        self.br = TransformBroadcaster(self)

    def callback(self, msg):

        x = msg.x
        y = msg.y
        theta = msg.theta

        pose = PoseWithCovarianceStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.pose.position.x = x
        pose.pose.pose.position.y = y

        qz = math.sin(theta/2)
        qw = math.cos(theta/2)

        pose.pose.pose.orientation.z = qz
        pose.pose.pose.orientation.w = qw

        self.pub.publish(pose)

        # TF broadcast
        t = TransformStamped()
        t.header.frame_id = "map"
        t.child_frame_id = "base_link"
        t.header.stamp = self.get_clock().now().to_msg()

        t.transform.translation.x = x
        t.transform.translation.y = y

        t.transform.rotation.z = qz
        t.transform.rotation.w = qw

        self.br.sendTransform(t)

        print(f"[Bridge] X:{x:.2f} Y:{y:.2f}")


def main():
    rclpy.init()
    node = PoseBridge()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()