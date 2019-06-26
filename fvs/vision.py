import fvs.utils as utils
import time
import cv2

class Vision:
    def __init__(self, ratio=None, size=None):
        """Initialize the Device given a ratio and size."""

        # Variables to hold the properties
        self._ratio = ratio
        self._size = size

        # Store the initial values for the vision frames in dictionary
        self._frames = {"prev": None, "curr": None}

    def __repr__(self):
        """Specify what to return when used as an input in the print() command."""

        # Return "class 'fvs.vision.Vision'>( list of frames )"
        functions = ', '.join(str(key) for key in self._frames.keys())
        return '{}({})'.format(type(self), functions)

    def __len__(self):
        """Specify what to return when used as an input in the len() command."""

        # Return the length of the frames dictionary
        return len(self._frames.items())

    def __setitem__(self, key, val):
        """Specify what to do when setting items using braket notation."""

        # Adds an item to the frames dictionary
        self._frames[key] = val

    def __getitem__(self, key):
        """Specify what to do when getting items using braket notation."""

        # Return the value from the frames dictionary at key
        return self._frames[key]

    def __iter__(self):
        """Specify what to do when a loop is used to iterate through."""

        # Returns an key, value iterator for the frames dictionary
        return iter(self._frames.items())

    def update(self, frames, focalpoint):
        """Update the original "prev" and "curr" frames and updates each vision."""

        # Crop and resize the "prev" frame from the original frame
        self._frames["prev"] = utils.cropRatio(frames["prev"], self._ratio, self._size, focalpoint)
        self._frames["prev"] = cv2.resize(self._frames["prev"], (self._size, self._size), interpolation=cv2.INTER_AREA)

        # Crop and resize the "curr" frame from the original frame
        self._frames["curr"] = utils.cropRatio(frames["curr"], self._ratio, self._size, focalpoint)
        self._frames["curr"] = cv2.resize(self._frames["curr"], (self._size, self._size), interpolation=cv2.INTER_CUBIC)

    def properties(self):
        """Get the properties for the Vision."""

        # Return the ratio and size specifications
        return self._ratio, self._size
