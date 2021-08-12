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


async def get_points(pipe):
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

    await asyncio.sleep(0.001)


async def myCoroutine():
    global lock

    pipe = rs.pipeline()
    cfg = rs.config()

    cfg.enable_stream(
        rs.stream.pose
    )  # Positional data (translation, rotation, velocity etc)
    cfg.enable_stream(rs.stream.fisheye, 1)  # Left camera
    cfg.enable_stream(rs.stream.fisheye, 2)  # Right camera

    pipe.start(cfg)

    while True:
        await get_points(pipe)

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(myCoroutine())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
