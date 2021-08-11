# Code from tutorialedge.net
# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/

import cv2
import math
import asyncio
import numpy as np
import pyrealsense2 as rs


class RST265(object):

    MAX_POINT_LEN = 500

    def __init__(self):
        self.pipe = rs.pipeline()

        self.cfg = rs.config()
        self.cfg.enable_stream(rs.stream.pose)
        self.cfg.enable_stream(rs.stream.fisheye, 1)  # Left camera
        self.cfg.enable_stream(rs.stream.fisheye, 2)  # Right camera

        self.pipe.start(self.cfg)
        self._cur_point = ()
        self._cur_vel = ()

        self._loop = asyncio.get_event_loop()

    def get_points(self):
        frames = self.pipe.wait_for_frames()

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

            self._cur_point = (pose_x, pose_y, pose_z)
            self._cur_vel = (vel_x, vel_y, vel_z)

    async def pose_coroutine(self):
        while True:
            self._loop.run_in_executor(None, self.get_points)
    
    def get_current_point(self):
        return self._cur_point

    def run(self):
        try:
            asyncio.ensure_future(self.pose_coroutine())
            self._loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self._loop.close()

if __name__=="__main__":
    t265 = RST265()
    t265.run()