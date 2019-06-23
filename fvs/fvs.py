import PIL.Image, PIL.ImageTk
import tkinter
import fvs.utils as utils
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
        self._devices[str(key)] = val

    def __getitem__(self, key):
        return self._devices[str(key)]

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

    def getFocalpoint(self):
        return self._focal_point


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

    def getProperties(self):
        return self._ratio, self._size

    def getFrames(self):
        return self._frames


class Application(tkinter.Tk):
    def __init__(self, fvs, *args, **kwargs):
        """Initialize the Application given FoveatedVisionSystem."""

        # Initialize the application as a tkinter object
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.configure(bg="lightgray")
        self.state('zoomed')

        # FoveatedVisionSystem to display in application
        self.fvs = fvs

        self.device = tkinter.StringVar(self)
        self.device_choices = [choice[0] for choice in self.fvs]
        self.device.set(self.device_choices[0])

        self.vision = tkinter.StringVar(self)
        self.vision_choices = [choice[0] for choice in self.fvs[self.device.get()]]
        self.vision.set(self.vision_choices[0])

        self.frame = tkinter.StringVar(self)
        self.frame_choices = [choice[0] for choice in self.fvs[self.device.get()][self.vision.get()]]
        self.frame.set(self.frame_choices[0])

        # Store the frames for the application
        self.app_frames = {}
        self.app_canvas = {}
        self.pil_frames = {}
        self.delay = 15

        # Create the master frame for the application
        self.title("Foveated Vision System")
        self.minsize(1200, 800)

        # Split the master frame into two left (west) and right (east) segments
        self.app_frames["west"] = tkinter.Frame(self, width=400, height=800, bg="lightgray")
        self.app_frames["east"] = tkinter.Frame(self, borderwidth=2, relief="solid", width=1200, height=800, bg="lightgray")

        # Split the west frame into two top (northwest, northeast)
        self.app_frames["northwest"] = tkinter.Frame(self.app_frames["west"], borderwidth=2, relief="solid", width=400, height=400, bg="lightgray")
        self.app_frames["southwest"] = tkinter.Frame(self.app_frames["west"], borderwidth=2, relief="solid", width=400, height=400, bg="lightgray")

        # Create the canvases to hold the video streams
        self.app_canvas["layered"] = tkinter.Canvas(self.app_frames["northwest"], width=400, height=400, bg="lightgray")
        self.app_canvas["stacked"] = tkinter.Canvas(self.app_frames["southwest"], width=200, height=400, scrollregion=(0,0,200,800), bg="lightgray")
        self.app_canvas["control"] = tkinter.Canvas(self.app_frames["east"], width=1200, height=800, bg="lightgray")

        # Set up scroll bar to scroll through frames
        self.scrollbar = tkinter.Scrollbar(self.app_frames["southwest"], bg="lightgray", command=self.app_canvas["stacked"].yview)
        self.app_canvas["stacked"].config(yscrollcommand=self.scrollbar.set)

        # Set up drop down menu to choose device
        self.dropdown_device = tkinter.OptionMenu(self.app_frames["east"], self.device, *self.device_choices)
        self.dropdown_device.config(width=200, background="lightgray")

        # Set up drop down menu to choose vision
        self.dropdown_vision = tkinter.OptionMenu(self.app_frames["east"], self.vision, *self.vision_choices)
        self.dropdown_vision.config(width=200, background="lightgray")

        # Set up drop down menu to choose frames
        self.dropdown_frame = tkinter.OptionMenu(self.app_frames["east"], self.frame, *self.frame_choices)
        self.dropdown_frame.config(width=200, background="lightgray")

        # Pack the frames into the application
        self.scrollbar.pack(side="right", fill="y")
        self.dropdown_device.pack(side="top")
        self.dropdown_vision.pack(side="top")
        self.dropdown_frame.pack(side="top")
        self.app_frames["west"].pack(side="left", fill="both")
        self.app_frames["east"].pack(side="right", fill="both", expand=True)
        self.app_frames["northwest"].pack(side="top", fill="both")
        self.app_frames["southwest"].pack(side="bottom", fill="both", expand=True)
        self.app_canvas["stacked"].pack(fill="both")
        self.app_canvas["layered"].pack(side="left", fill="both", expand=True)
        self.app_canvas["control"].pack(fill="both", expand=True)

    def update(self):
        self.fvs.update()

        self.device.trace('w', self.update_device)
        self.device.trace('w', self.update_vision)

        # Create the blank images
        layered = PIL.Image.new('RGBA', (400, 400))
        stacked = PIL.Image.new('RGBA', (200, 800))
        control = PIL.Image.new('RGBA', (1200, 800))

        # Get the stack and layered images from the frames
        i = 0

        # Loop through the visions in a device
        for vision_key, vision in self.fvs[self.device.get()]:

            # Loop through the frames in a vision
            for frame_key, frame in vision:

                # Get the properties and turn the image into RGBA
                ratio, size = vision.getProperties()
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

                # Paste the images together in layered
                img_frame = PIL.Image.fromarray(cv2.resize(rgb_frame, (int(400 * ratio), int(400 * ratio))))
                layered.paste(img_frame, (int(200 * (1 - ratio)), int(200 * (1 - ratio))))

                # Paste the images together in stacked
                img_frame = PIL.Image.fromarray(cv2.resize(rgb_frame, (200, 200)))
                stacked.paste(img_frame, (0, 200 * i))
            i += 1

        # Add the stacked image to the canvas
        self.pil_frames["stacked"] = PIL.ImageTk.PhotoImage(image=stacked)
        self.app_canvas["stacked"].create_image(100, 0, image=self.pil_frames["stacked"], anchor=tkinter.NW)

        # Add the layered image to the canvas
        self.pil_frames["layered"] = PIL.ImageTk.PhotoImage(image=layered)
        self.app_canvas["layered"].create_image(0, 0, image=self.pil_frames["layered"], anchor=tkinter.NW)

        # Add the control image to the canvas
        img_frame = cv2.cvtColor(self.fvs[self.device.get()][self.vision.get()][self.frame.get()], cv2.COLOR_BGR2RGBA)
        control = PIL.Image.fromarray(cv2.resize(img_frame, (1200, 800)))
        self.pil_frames["control"] = PIL.ImageTk.PhotoImage(image=control)
        self.app_canvas["control"].create_image(0, 0, image=self.pil_frames["control"], anchor=tkinter.NW)

        # Continue to update
        self.after(self.delay, self.update)

    def update_device(self, *args):
        self.vision_choices = [choice[0] for choice in self.fvs[self.device.get()]]
        self.vision.set(self.vision_choices[0])
        menu = self.dropdown_vision["menu"]
        menu.delete(0, "end")
        for string in self.vision_choices:
            menu.add_command(label=string, command=lambda value=string: self.vision.set(value))

    def update_vision(self, *args):
        self.frame_choices = [choice[0] for choice in self.fvs[self.device.get()][self.vision.get()]]
        self.frame.set(self.frame_choices[0])
        menu = self.dropdown_frame["menu"]
        menu.delete(0, "end")
        for string in self.frame_choices:
            menu.add_command(label=string, command=lambda value=string: self.frame.set(value))
