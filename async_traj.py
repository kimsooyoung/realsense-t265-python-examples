# Code from tutorialedge.net
# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/

import cv2
import math
import asyncio
import numpy as np
import pyrealsense2 as rs


from collections import deque


lock = asyncio.Lock()

MAX_POINT_LEN = 500
point_deq = deque(maxlen=MAX_POINT_LEN)

map_width, map_height = (600, 600)
map_scale = 1


def get_points(pipe):
    global point_deq

    frames = pipe.wait_for_frames()

    # Positional data frame
    pose = frames.get_pose_frame()
    if pose:
        pose_data = pose.get_pose_data()

        vel_x = pose_data.velocity.x
        vel_y = pose_data.velocity.y
        vel_z = pose_data.velocity.z

        pose_x = pose_data.translation.x
        pose_y = pose_data.translation.y
        pose_z = pose_data.translation.z

        point_x = int(300 * pose_x) + 300
        point_z = int(300 * pose_z) + 300

        point_deq.append((point_x, point_z))
        print(list(point_deq)[-1], len(point_deq))

        traj = np.zeros((map_width, map_height, 3), dtype=np.uint8)
        cv2.rectangle(traj, (10, 20), (600, 60), (0, 0, 0), -1)

        # # pose_x * -1 to make forward positive
        text = "Coordinates: x=%2fm z=%2fm" % (-1 * pose_x, pose_z)
        cv2.putText(
            traj, "text", (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 8
        )

        for point in point_deq:
            cv2.circle(traj, point, 1, (0, 255, 0), 1)

        # cv2.imshow("Trajectory", traj)
        # cv2.waitKey(1)


def draw_points():
    global point_deq

    traj = np.zeros((map_width, map_height, 3), dtype=np.uint8)
    cv2.rectangle(traj, (10, 20), (600, 60), (0, 0, 0), -1)

    # # pose_x * -1 to make forward positive
    # text = "Coordinates: x=%2fm z=%2fm" % (-1 * pose_x, pose_z)
    cv2.putText(
        traj, "sdfs", (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 8
    )

    for point in point_deq:
        cv2.circle(traj, point, 1, (0, 255, 0), 1)

    cv2.imshow("Trajectory", traj)
    cv2.waitKey(1)


async def myCoroutine():
    global lock

    # Get realsense pipeline handle
    pipe = rs.pipeline()

    # Configure the pipeline
    cfg = rs.config()

    # Enable streams you are interested in
    cfg.enable_stream(
        rs.stream.pose
    )  # Positional data (translation, rotation, velocity etc)
    cfg.enable_stream(rs.stream.fisheye, 1)  # Left camera
    cfg.enable_stream(rs.stream.fisheye, 2)  # Right camera

    # Start the configured pipeline
    pipe.start(cfg)

    # async with lock:
    while True:
        await loop.run_in_executor(None, get_points, pipe)


async def mySecondCoroutine():
    global lock

    async with lock:
        while True:
            await loop.run_in_executor(None, draw_points)
        # cv2.waitKey(1)


loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(myCoroutine())
    # asyncio.ensure_future(mySecondCoroutine())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
