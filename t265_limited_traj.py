# Basic Python Interface code with Intel-Realesne T265
#
# this code is refered from below repository
# https://github.com/markku-ai/realsense-t265


# This assumes .so file is found on the same directory
import pyrealsense2 as rs

from collections import deque
from pprint import pprint
import numpy as np
import cv2

# Get realsense pipeline handle
pipe = rs.pipeline()

# Configure the pipeline
cfg = rs.config()

# Prints a list of available streams, not all are supported by each device
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

MAX_POINT_LEN = 500
point_deq = deque(maxlen=MAX_POINT_LEN)


async def get_points():
    global point_deq

    while True:
        frames = pipe.wait_for_frames()

        # Positional data frame
        pose = frames.get_pose_frame()
        if pose:
            pose_data = pose.get_pose_data()
            # print("\nFrame number: ", pose.frame_number)
            # print("Position: ", pose_data.translation)
            # print("Velocity: ", pose_data.velocity)
            # print("Acceleration: ", pose_data.acceleration)
            # print("Rotation: ", pose_data.rotation)

            vel_x = pose_data.velocity.x
            vel_y = pose_data.velocity.y
            vel_z = pose_data.velocity.z

            pose_x = pose_data.translation.x
            pose_y = pose_data.translation.y
            pose_z = pose_data.translation.z

            point_x = int(300 * pose_x) + 300
            point_z = int(300 * pose_z) + 300

            point_deq.append((point_x, point_z))

            traj = np.zeros((map_width, map_height, 3), dtype=np.uint8)
            cv2.rectangle(traj, (10, 20), (600, 60), (0, 0, 0), -1)

            # pose_x * -1 to make forward positive
            text = "Coordinates: x=%2fm z=%2fm" % (-1 * pose_x, pose_z)
            cv2.putText(
                traj, text, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 8
            )

            for point in point_deq:
                cv2.circle(traj, point, 1, (0, 255, 0), 1)

            cv2.imshow("Trajectory", traj)

        cv2.waitKey(1)


async def mySecondCoroutine():
    global lock, counter

    async with lock:
        while True:
            counter += 1
            await asyncio.sleep(1)
            print(f"I am mySecondCoroutine, And Current Counter is {counter} ")


try:
    while True:
        frames = pipe.wait_for_frames()

        # Positional data frame
        pose = frames.get_pose_frame()
        if pose:
            pose_data = pose.get_pose_data()
            # print("\nFrame number: ", pose.frame_number)
            # print("Position: ", pose_data.translation)
            # print("Velocity: ", pose_data.velocity)
            # print("Acceleration: ", pose_data.acceleration)
            # print("Rotation: ", pose_data.rotation)

            vel_x = pose_data.velocity.x
            vel_y = pose_data.velocity.y
            vel_z = pose_data.velocity.z

            pose_x = pose_data.translation.x
            pose_y = pose_data.translation.y
            pose_z = pose_data.translation.z

            point_x = int(300 * pose_x) + 300
            point_z = int(300 * pose_z) + 300

            point_deq.append((point_x, point_z))

            traj = np.zeros((map_width, map_height, 3), dtype=np.uint8)
            cv2.rectangle(traj, (10, 20), (600, 60), (0, 0, 0), -1)

            # pose_x * -1 to make forward positive
            text = "Coordinates: x=%2fm z=%2fm" % (-1 * pose_x, pose_z)
            cv2.putText(
                traj, text, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 8
            )

            for point in point_deq:
                cv2.circle(traj, point, 1, (0, 255, 0), 1)

            cv2.imshow("Trajectory", traj)

        cv2.waitKey(1)
finally:
    pipe.stop()
