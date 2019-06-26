import fvs.utils as utils
import cv2

class Device(cv2.VideoCapture):
    def __init__(self, index, *args, **kwargs):
        """Initialize the Device given a capture device index."""

        # Initialize the device as a cv2.VideoCapture object
        cv2.VideoCapture.__init__(self, index, *args, **kwargs)

        # Variables to hold the properties
        self._focalpoint = [0, 0]

        # Store the initial values for the original frames in dictionary
        self._frames = {}
        self._frames["prev"] = utils.cropSquare(self.read()[1])
        self._frames["curr"] = utils.cropSquare(self.read()[1])

        # Create an empty dictionary to hold the visions
        self._visions = {}

    def __repr__(self):
        """Specify what to return when used as an input in the print() command."""

        # Return "class 'fvs.device.Device'>( list of visions )"
        visions = ', '.join(str(key) for key in self._visions.keys())
        return '{}({})'.format(type(self), visions)

    def __len__(self):
        """Specify what to return when used as an input in the len() command."""

        # Return the length of the visions dictionary
        return len(self._visions)

    def __setitem__(self, key, val):
        """Specify what to do when setting items using braket notation."""

        # Adds an item to the visions dictionary and updates the vision
        self._visions[key] = val
        self._visions[key].update(self._frames, self._focalpoint)

    def __getitem__(self, key):
        """Specify what to do when getting items using braket notation."""

        # Return the value from the visions dictionary at key
        return self._visions[key]

    def __iter__(self):
        """Specify what to do when a loop is used to iterate through."""

        # Returns an key, value iterator for the visions dictionary
        return iter(self._visions.items())

    def update(self):
        """Update the original "prev" and "curr" frames and updates each vision."""

        # Update the original "prev" and "curr" frames
        self._frames["prev"] = self._frames["curr"]
        self._frames["curr"] = utils.cropSquare(self.read()[1])

        # Update each vision in device
        for vision in self._visions.values():
            vision.update(self._frames, self._focalpoint)

    def focalpoint(self):
        """Returns the focal point (center of view for the device)."""

        # Returns the focal point
        return self._focalpoint

    def original(self):
        """Return the original curr and prev frmaes."""

        # Return the _frames
        return self._frames
