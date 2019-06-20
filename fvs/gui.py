import PIL.Image, PIL.ImageTk
import fvs_utils as utils
import tkinter
import cv2

class Application(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        """Initialize the Application given multiple camera indices."""

        # Initialize the application as a tkinter object
        tkinter.Frame.__init__(self, master, *args, **kwargs)

        # Store the frames for the application
        self.app_frames = {}
        self.app_canvas = {}
        self.pil_frames = {}
        self.delay = 15

        # Create the master frame for the application
        self.app_frames["master"] = master
        self.app_frames["master"].title("Foveated Vision System")
        self.app_frames["master"].minsize(750, 750)
        self.app_frames["master"].resizable(False, False)

        # Split the master frame into two left (west) and right (east) segments
        self.app_frames["west"] = tkinter.Frame(self.app_frames["master"])
        self.app_frames["east"] = tkinter.Frame(self.app_frames["master"])

        # Split the west and east frames into two top (northwest, northeast) and bottom (southwest, southeast) segments
        self.app_frames["northwest"] = tkinter.Frame(self.app_frames["west"], borderwidth=2, relief="solid")
        self.app_frames["northeast"] = tkinter.Frame(self.app_frames["east"], borderwidth=2, relief="solid")
        self.app_frames["southwest"] = tkinter.Frame(self.app_frames["west"], borderwidth=2, relief="solid")
        self.app_frames["southeast"] = tkinter.Frame(self.app_frames["east"], borderwidth=2, relief="solid")

        # Pack the frames into the application
        self.app_frames["west"].pack(side="left", fill="both", expand=True)
        self.app_frames["east"].pack(side="right", fill="both", expand=True)
        self.app_frames["northwest"].pack(side="top", fill="both", expand=True)
        self.app_frames["northeast"].pack(side="top", fill="both", expand=True)
        self.app_frames["southwest"].pack(side="bottom", fill="both", expand=True)
        self.app_frames["southeast"].pack(side="bottom", fill="both", expand=True)

        # Create the prev and curr canvas for displaying the video
        self.app_canvas["prev"] = tkinter.Canvas(self.app_frames["northwest"], width=200, height=200)
        self.app_canvas["curr"] = tkinter.Canvas(self.app_frames["northwest"], width=200, height=200)

        # Pack the canvas into the application
        self.app_canvas["prev"].pack()
        self.app_canvas["curr"].pack()

        # Store the capture for the device
        self.camera_index = 0
        self.video_capture = cv2.VideoCapture(self.camera_index)

        # Store the current and previous frames
        self.cap_frames = {"prev": None, "curr": None}
        self.cap_frames["prev"] = utils.cropSquare(self.video_capture.read()[1])
        self.cap_frames["curr"] = utils.cropSquare(self.video_capture.read()[1])

        # Set the focal point to the origin of the capture
        self.focal_point = [0, 0]

        # Create an empty containapp_er to store FoveatedVision objects
        self.visions = {}

    def update(self):
        """Update the application window to stream the video captures."""

        # Update the frames for the capture device
        self.cap_frames["prev"] = self.cap_frames["curr"]
        self.cap_frames["curr"] = utils.cropSquare(self.video_capture.read()[1])

        # Swap color channels from BGR to RGB
        prev = cv2.resize(cv2.cvtColor(self.cap_frames["prev"], cv2.COLOR_BGR2RGB), (200, 200))
        curr = cv2.resize(cv2.cvtColor(self.cap_frames["curr"], cv2.COLOR_BGR2RGB), (200, 200))

        # Convert frames to PIL frames
        self.pil_frames["prev"] = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(prev))
        self.pil_frames["curr"] = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(curr))

        # Update canvas to stream video
        self.app_canvas["prev"].create_image(0, 0, image=self.pil_frames["prev"], anchor=tkinter.NW)
        self.app_canvas["curr"].create_image(0, 0, image=self.pil_frames["curr"], anchor=tkinter.NW)

        # Continue to update
        self.app_frames["master"].after(self.delay, self.update)

class FoveatedVision:
    def __init__(self, ratio, pixels, focal_point):
        """Initialize the FoveatedVision given a ratio, pixels, and focal point."""
        self.ratio = ratio
        self.pixels = pixels
        self.focal_point = focal_point
        self.frames = {}
        self.tasks = {}
        self.networks = {}


root = tkinter.Tk()
app = Application(root)
app.update()
app.mainloop()
