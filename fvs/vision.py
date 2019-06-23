import fvs.utils as utils
import cv2

class Vision:
    def __init__(self, ratio=None, size=None):
        self._ratio = ratio
        self._size = size
        self._frames = {"prev": None, "curr": None}

    def __repr__(self):
        functions = ', '.join(str(key) for key in self._frames.keys())
        return '{}({})'.format(type(self), functions)

    def __len__(self):
        return len(self._frames.items())

    def __setitem__(self, key, val):
        self._frames[key] = val

    def __getitem__(self, key):
        return self._frames[key]

    def __iter__(self):
        return iter(self._frames.items())

    def update(self, frames, focal_point):
        self._frames["prev"] = utils.cropRatio(frames["prev"], self._ratio, self._size, focal_point)
        self._frames["prev"] = cv2.resize(self._frames["prev"], (self._size, self._size))

        self._frames["curr"] = utils.cropRatio(frames["curr"], self._ratio, self._size, focal_point)
        self._frames["curr"] = cv2.resize(self._frames["curr"], (self._size, self._size))

    def getProperties(self):
        return self._ratio, self._size

    def getFrames(self):
        return self._frames
