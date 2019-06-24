import fvs.utils as utils
import cv2

class System():
    def __init__(self, *args, **kwargs):
        """Initialize the System."""

        # Create an empty dictionary to hold the devices
        self._devices = {}

    def __repr__(self):
        """Specify what to return when used as an input in the print() command."""

        # Return "class 'fvs.system.System'>( list of devices )"
        devices = ', '.join(str(key) for key in self._devices.keys())
        return '{}({})'.format(type(self), devices)

    def __len__(self):
        """Specify what to return when used as an input in the len() command."""

        # Return the length of the devices dictionary
        return len(self._devices)

    def __setitem__(self, key, val):
        """Specify what to do when setting items using braket notation."""

        # Adds an item to the devices dictionary
        self._devices[str(key)] = val

    def __getitem__(self, key):
        """Specify what to do when getting items using braket notation."""

        # Return the value from the devices dictionary at key
        return self._devices[str(key)]

    def __iter__(self):
        """Specify what to do when a loop is used to iterate through."""

        # Returns an key, value iterator for the devices dictionary
        return iter(self._devices.items())

    def update(self):
        """Update each device."""

        # Update each device inside the devices dictionary
        for device in self._devices.values():
            device.update()
