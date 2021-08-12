# Code from tutorialedge.net
# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/

import cv2
import math
import asyncio
import numpy as np
import pyrealsense2 as rs


class RST265(object):

    MAX_POINT_LEN = 500
    DEBUG_MODE = True

    def __init__(self):
        self._pipe = rs.pipeline()

        self._cfg = rs.config()
        self._cfg.enable_stream(rs.stream.pose)
        self._cfg.enable_stream(rs.stream.fisheye, 1)  # Left camera
        self._cfg.enable_stream(rs.stream.fisheye, 2)  # Right camera

        self._cur_pose = ()
        self._cur_vel = ()

        self._loop = asyncio.get_event_loop()

    def pipe_start(self):
        self._pipe.start(self._cfg)
        if self.DEBUG_MODE is True:
            print("Start Pipe")

    def pipe_stop(self):
        self._pipe.stop()
        if self.DEBUG_MODE is True:
            print("Stop Pipe")

    async def get_pose_data(self):
        frames = self._pipe.wait_for_frames()

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

            self._cur_pose = (pose_x, pose_y, pose_z)
            self._cur_vel = (vel_x, vel_y, vel_z)
            
            # print("\nFrame number: ", pose.frame_number)
            # print(self._cur_pose)
            # print(self._cur_vel)

            await asyncio.sleep(0.0005)

        return (self._cur_pose, self._cur_vel)


    async def pose_coroutine(self):
        while True:
            await self.get_pose_data()

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
            print("====== Loop Closed =========")

if __name__=="__main__":

    t265 = RST265()
    try:
        t265.pipe_start()
        t265.run()
    except Exception as e:
        print(e)
    finally:
        t265.pipe_stop()
        print("Done...")