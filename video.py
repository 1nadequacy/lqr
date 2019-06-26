import imageio
import os
import numpy as np


class VideoRecorder(object):
    def __init__(self,
                 env,
                 enabled=True,
                 height=256,
                 width=256,
                 cameras=[0],
                 fps=30):
        self._env = env
        self._enabled = enabled
        self._height = height
        self._width = width
        self._cameras = cameras
        self._fps = fps
        self._frames = []

    def _make_grid(self, images):
        n = len(images)
        if n == 1:
            return images[0]
        assert n % 2 == 0
        top_row = np.concatenate(images[:n // 2], axis=1)
        bottom_row = np.concatenate(images[n // 2:], axis=1)
        grid = np.concatenate([top_row, bottom_row], axis=0)
        return grid

    def record(self):
        if self._enabled:
            images = []
            for camera_id in self._cameras:
                frame = self._env.render(
                    mode='rgb_array',
                    height=self._height,
                    width=self._width,
                    camera_id=camera_id)
                images.append(frame)
            self._frames.append(self._make_grid(images))

    def save(self, dir_name, file_name):
        if self._enabled:
            path = os.path.join(dir_name, file_name)
            imageio.mimsave(path, self._frames, fps=self._fps)
