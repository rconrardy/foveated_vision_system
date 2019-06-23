import fvs.utils as utils
import cv2

class System():
    def __init__(self, *args, **kwargs):
        self._devices = {}

    def __repr__(self):
        devices = ', '.join(str(key) for key in self._devices.keys())
        return '{}({})'.format(type(self), devices)

    def __len__(self):
        return len(self._devices)

    def __setitem__(self, key, val):
        self._devices[str(key)] = val

    def __getitem__(self, key):
        return self._devices[str(key)]

    def __iter__(self):
        return iter(self._devices.items())

    def update(self):
        for device in self._devices.values():
            device.update()
