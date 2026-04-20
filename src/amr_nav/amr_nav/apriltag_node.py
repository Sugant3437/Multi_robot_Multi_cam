#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from amr_interfaces.msg import RobotPose

import cv2
import numpy as np
from pupil_apriltags import Detector
import math

class AprilTagNode(Node):

    def __init__(self):
        super().__init__('apriltag_node')

        self.pub = self.create_publisher(RobotPose, '/robot_pose_cam', 10)

        self.cap = cv2.VideoCapture("http://192.168.5.106:81/stream")
        self.detector = Detector(families="tag36h11")

        self.timer = self.create_timer(0.1, self.process)

    def process(self):

        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.resize(frame, (640,480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detections = self.detector.detect(gray)

        for tag in detections:

            cx, cy = tag.center

            # 🔥 SIMPLE SCALE (ADJUST THIS ONCE)
            SCALE = 0.002

            dx = cx - 320
            dy = cy - 240

            x = dx * SCALE
            y = dy * SCALE

            pt1 = tag.corners[0]
            pt2 = tag.corners[1]

            theta = math.atan2(pt2[1]-pt1[1], pt2[0]-pt1[0])

            msg = RobotPose()
            msg.x = float(x)
            msg.y = float(y)
            msg.theta = float(theta)

            self.pub.publish(msg)

            print(f"[AprilTag] X:{x:.2f} Y:{y:.2f} θ:{theta:.2f}")

            break


def main():
    rclpy.init()
    node = AprilTagNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
