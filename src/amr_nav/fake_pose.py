import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
import math

class FakePose(Node):

    def __init__(self):
        super().__init__('fake_pose')

        self.pub = self.create_publisher(PoseWithCovarianceStamped, '/amcl_pose', 10)
        self.timer = self.create_timer(0.5, self.publish_pose)

        self.x = 0.0
        self.y = 0.0

    def publish_pose(self):

        self.x += 0.05   # simulate movement

        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = "map"
        msg.header.stamp = self.get_clock().now().to_msg()

        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y

        msg.pose.pose.orientation.w = 1.0

        self.pub.publish(msg)

        print(f"Fake Pose: {self.x:.2f}, {self.y:.2f}")


def main():
    rclpy.init()
    node = FakePose()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()