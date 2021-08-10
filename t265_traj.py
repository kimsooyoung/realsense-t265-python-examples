# Basic Python Interface code with Intel-Realesne T265
#
# this code is refered from below repository
# https://github.com/markku-ai/realsense-t265

# This assumes .so file is found on the same directory
import pyrealsense2 as rs

# Prettier prints for reverse-engineering
from pprint import pprint
import numpy as np
import cv2

# Get realsense pipeline handle
pipe = rs.pipeline()

# Configure the pipeline
cfg = rs.config()

# Prints a list of available streams, not all are supported by each device
print("Available streams:")
pprint(dir(rs.stream))
#  'accel', 'any', 'color', 'confidence', 'depth',
#  'fisheye', 'gpio', 'gyro', 'infrared', 'name',
#  'pose', 'value'

# Enable streams you are interested in
cfg.enable_stream(
    rs.stream.pose
)  # Positional data (translation, rotation, velocity etc)
cfg.enable_stream(rs.stream.fisheye, 1)  # Left camera
cfg.enable_stream(rs.stream.fisheye, 2)  # Right camera

# Start the configured pipeline
pipe.start(cfg)

# traj setup
map_width, map_height = (600, 600)
map_scale = 1
traj = np.zeros((map_width, map_height, 3), dtype=np.uint8)

try:
    for _ in range(1000):
        frames = pipe.wait_for_frames()

        # Left fisheye camera frame
        left = frames.get_fisheye_frame(1)
        left_data = np.asanyarray(left.get_data())

        # Right fisheye camera frame
        right = frames.get_fisheye_frame(2)
        right_data = np.asanyarray(right.get_data())

        print("Left frame", left_data.shape)
        print("Right frame", right_data.shape)

        # cv2.imshow('left', left_data)
        # cv2.imshow('right', right_data)

        # Positional data frame
        pose = frames.get_pose_frame()
        if pose:
            pose_data = pose.get_pose_data()
            print("\nFrame number: ", pose.frame_number)
            print("Position: ", pose_data.translation)
            print("Velocity: ", pose_data.velocity)
            print("Acceleration: ", pose_data.acceleration)
            print("Rotation: ", pose_data.rotation)

            pose_x = pose_data.translation.x
            pose_z = pose_data.translation.z

            point_x = int(300 * pose_x) + 300
            point_z = int(300 * pose_z) + 300

            cv2.rectangle(traj, (10, 20), (600, 60), (0, 0, 0), -1)
            text = "Coordinates: x=%2fm z=%2fm" % (pose_x, pose_z)
            cv2.putText(
                traj, text, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 8
            )

            cv2.circle(traj, (point_x, point_z), 1, (0, 255, 0), 1)
            cv2.imshow("Trajectory", traj)

        cv2.waitKey(1)
finally:
    pipe.stop()
