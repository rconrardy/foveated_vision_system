import fvs.utils as utils
import cv2

class Device(cv2.VideoCapture):
    def __init__(self, index, *args, **kwargs):
        cv2.VideoCapture.__init__(self, index, *args, **kwargs)
        self._focal_point = [0, 0]
        self._frames = {"curr": utils.cropSquare(self.read()[1])}
        self._visions = {}

    def __repr__(self):
        visions = ', '.join(str(key) for key in self._visions.keys())
        return '{}({})'.format(type(self), visions)

    def __len__(self):
        return len(self._visions)

    def __setitem__(self, key, val):
        self._visions[key] = val
        self._visions[key].update(self._frames, self._focal_point)

    def __getitem__(self, key):
        return self._visions[key]

    def __iter__(self):
        return iter(self._visions.items())

    def update(self):
        self._frames["curr"] = utils.cropSquare(self.read()[1])
        for vision in self._visions.values():
            vision.update(self._frames, self._focal_point)

    def getFocalpoint(self):
        return self._focal_point
