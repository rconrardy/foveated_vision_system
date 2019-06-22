import PIL.Image, PIL.ImageTk
import tkinter
import utils
import cv2

class FoveatedVisionSystem():
    def __init__(self, *args, **kwargs):
        self._devices = {}

    def __repr__(self):
        devices = ', '.join(str(key) for key in self._devices.keys())
        return '{}({})'.format(type(self), devices)

    def __len__(self):
        return len(self._devices)

    def __setitem__(self, key, val):
        self._devices[key] = val

    def __getitem__(self, key):
        return self._devices[key]

    def __iter__(self):
        return iter(self._devices.items())

    def update(self):
        for device in self._devices.values():
            device.update()


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


class Vision:
    def __init__(self, ratio=None, size=None):
        self._ratio = ratio
        self._size = size
        self._frames = {"curr": None}

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
        self._frames["curr"] = utils.cropRatio(frames["curr"], self._ratio, self._size, focal_point)
        self._frames["curr"] = cv2.resize(self._frames["curr"], (self._size, self._size))

    def getFrames(self):
        return self._frames


class Application(tkinter.Tk):
    def __init__(self, fvs, *args, **kwargs):
        """Initialize the Application given FoveatedVisionSystem."""

        # Initialize the application as a tkinter object
        tkinter.Tk.__init__(self, *args, **kwargs)

        # FoveatedVisionSystem to display in application
        self.fvs = fvs

        # Store the frames for the application
        self.cap_frames = {}
        self.app_frames = {}
        self.app_canvas = {}
        self.pil_frames = {}
        self.delay = 15

        # Create the master frame for the application
        self.title("Foveated Vision System")
        self.minsize(1000, 750)
        # self.resizable(False, False)

        # Split the master frame into two left (west) and right (east) segments
        self.app_frames["west"] = tkinter.Frame(self)
        self.app_frames["east"] = tkinter.Frame(self, borderwidth=2, relief="solid")

        # Split the west and east frames into two top (northwest, northeast) and bottom (southwest, southeast) segments
        self.app_frames["northwest"] = tkinter.Frame(self.app_frames["west"], borderwidth=2, relief="solid")
        self.app_frames["southwest"] = tkinter.Frame(self.app_frames["west"], borderwidth=2, relief="solid")

        # Pack the frames into the application
        self.app_frames["west"].pack(side="left", fill="both", expand=True)
        self.app_frames["east"].pack(side="right", fill="both", expand=True)
        self.app_frames["northwest"].pack(side="top", fill="both", expand=True)
        self.app_frames["southwest"].pack(side="bottom", fill="both", expand=True)

        # Create the prev and curr canvas for displaying the video
        for vision_key, vision in self.fvs[0]:
            for frame_key, frame in vision:
                self.app_canvas[frame_key] = tkinter.Canvas(self.app_frames["southwest"], width=400, height=400)
        self.app_canvas["northwest"] = tkinter.Canvas(self.app_frames["northwest"], width=400, height=400)

        # Pack the canvas into the application
        self.app_canvas["northwest"].pack()

    def update(self):
        self.fvs.update()

        northwest = PIL.Image.new('RGB', (400, 400))

        i = 0
        val = [4/4, 3/4, 2/4, 1/4]

        for vision_key, vision in self.fvs[0]:
            self.cap_frames[vision_key] = {}
            for frame_key, frame in vision:
                self.cap_frames[frame_key] = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (int(400 * val[i]), int(400 * val[i])))
                self.cap_frames[frame_key] = PIL.Image.fromarray(self.cap_frames[frame_key])
                northwest.paste(self.cap_frames[frame_key], (int(200 * (1 - val[i])), int(200 * (1 - val[i]))))
            i += 1

        self.pil_frames["northwest"] = PIL.ImageTk.PhotoImage(image=northwest)
        self.app_canvas["northwest"].create_image(0, 0, image=self.pil_frames["northwest"], anchor=tkinter.NW)




        # for device_key, device in self.fvs:
        #     for vision_key, vision in device:
        #         self.cap_frames[vision_key] = vision.getFrames()
        #
        # # Swap color channels from BGR to RGB
        # northwest = PIL.Image.new('RGB', (200, 200))
        # for vision in self.cap_frames.values():
        #     prev = cv2.resize(cv2.cvtColor(vision["prev"], cv2.COLOR_BGR2RGB), (200, 200))
        #     curr = cv2.resize(cv2.cvtColor(vision["curr"], cv2.COLOR_BGR2RGB), (200, 200))
        #
        #     # Conve rt nparray into PIL images
        #     prev = PIL.Image.fromarray(prev)
        #     curr = PIL.Image.fromarray(curr)
        #
        #     # Paste the images together
        #     northwest.paste(curr, (20, 0))
        #
        # # Convert frames to PIL frames
        # self.pil_frames["northwest"] = PIL.ImageTk.PhotoImage(image=northwest)
        #
        # # Update canvas to stream video
        # self.app_canvas["northwest"].create_image(0, 0, image=self.pil_frames["northwest"], anchor=tkinter.NW)
        #
        # # Continue to update
        self.after(self.delay, self.update)
