import cv2
import asyncio
import numpy as np

from t265_class import RST265


map_width, map_height = (600, 600)
map_scale = 1
traj = np.zeros((map_width, map_height, 3), dtype=np.uint8)

class Wrapper(object):

    def __init__(self):
        self._t265 = RST265()
        self._loop = asyncio.get_event_loop()

    async def print_pose(self):
        self._t265.pipe_start()

        while True:
            pose_data, vel_data = await self._t265.get_pose_data()
            # print(pose_data)
            # print(vel_data)

            pose_x, _, pose_z = pose_data

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

    def run(self):
        asyncio.ensure_future(self.print_pose())
        self._loop.run_forever()

    def __del__(self):
        self._t265.pipe_stop()

if __name__=="__main__":
    my_class = Wrapper()

    try:
        my_class.run()
    except KeyboardInterrupt:
        pass
    finally:
        print("Done...")