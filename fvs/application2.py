import PIL.Image, PIL.ImageTk
import tkinter
import cv2

class Application(tkinter.Tk):
    def __init__(self, system, *args, **kwargs):
        """Initialize the Application given a system."""

        # Initialize the application as a tkinter.Tk object
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Foveated Vision System")
        self.configure(bg="black", width=1000, height=840)
        self.resizable(width=False, height=False)

        # Store the system to display in application
        self._system = system

        # Store all the information for the application as dictionaries
        self._appFrames = {}
        self._appOption = {}
        self._appChoice = {}
        self._appString = {}
        self._appTracer = {}
        self._appCanvas = {}
        self._pilFrames = {}

        # set up drop down menu for choosing a device
        self._appString["device"] = tkinter.StringVar(self)
        self._appChoice["device"] = [choice[0] for choice in self._system]
        self._appString["device"].set(self._appChoice["device"][0])

        # set up drop down menu for choosing a vision
        self._appString["vision"] = tkinter.StringVar(self)
        self._appChoice["vision"] = [choice[0] for choice in self._system[self._appString["device"].get()]]
        self._appString["vision"].set(self._appChoice["vision"][0])

        # set up drop down menu for choosing a frame
        self._appString["frame"] = tkinter.StringVar(self)
        self._appChoice["frame"] = [choice[0] for choice in self._system[self._appString["device"].get()][self._appString["vision"].get()]]
        self._appString["frame"].set(self._appChoice["frame"][0])

        self._appFrames["west"] = tkinter.Frame(self, bd=20, width=400, height=850, bg="white")
        self._appFrames["cent"] = tkinter.Frame(self, bd=20, width=200, height=850, bg="white")
        self._appFrames["east"] = tkinter.Frame(self, bd=20, width=400, height=850, bg="white")
        self._appFrames["west"].pack(side="left", fill="both", expand=True)
        self._appFrames["cent"].pack(side="left", fill="both", expand=True)
        self._appFrames["east"].pack(side="left", fill="both", expand=True)

        self._appCanvas["control"] = tkinter.Canvas(self._appFrames["west"], bd=-2, width=400, height=850, bg="white")
        self._appCanvas["layered"] = tkinter.Canvas(self._appFrames["east"], bd=-2, width=400, height=850, bg="white")
        self._appCanvas["stacked"] = tkinter.Canvas(self._appFrames["cent"], bd=-2, width=200, height=850, bg="white")

        # self.scrollbar = tkinter.Scrollbar(self._appFrames["cent"], command=self._appCanvas["stacked"].yview)
        # self.scrollbar.pack(side="right", fill="y")

        # self._appCanvas["stacked"].config(yscrollcommand=self.scrollbar.set)
        self._appCanvas["control"].pack(side="left", fill="both", expand=True)
        self._appCanvas["stacked"].pack(side="left", fill="both", expand=True)
        self._appCanvas["layered"].pack(side="left", fill="both", expand=True)

        self.update()

    def update(self):

        # Update the vision frames in the system
        self._system.update()

        focalpoint = self._system[self._appString["device"].get()].focalpoint()

        control = PIL.Image.new('RGBA', (400, 400), (0, 0, 0, 255))
        stacked = PIL.Image.new('RGBA', (200, 2000), (255, 255, 255, 0))
        layered = PIL.Image.new('RGBA', (400, 400), (0, 0, 0, 255))

        visionList = [(visionKey, vision) for visionKey, vision in self._system[self._appString["device"].get()]]

        boxes = []
        # Loop through each vision in the vision list
        for i, (visionKey, vision) in enumerate(visionList):

            # Grab the frames from the vision when it is "curr"
            frameList = [frame for frameKey, frame in vision if frameKey==self._appString["frame"].get()]

            # Loop through each frame in the frame list
            for frame in frameList:

                ratio, size = vision.properties()
                rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                boxes.append([])
                # print(rgbFrame.shape)
                width, height, channels = rgbFrame.shape

                # Paste the images together in layered
                imgFrame = PIL.Image.fromarray(cv2.resize(rgbFrame, (200, 200)))
                stacked.paste(imgFrame, (0, 210 * i))

                imgFrame = PIL.Image.fromarray(cv2.resize(rgbFrame, (int(400 * ratio), int(400 * ratio))))
                layered.paste(imgFrame, (int(200 * (1 - ratio)), int(200 * (1 - ratio))))

        # Add the stacked image to the canvas
        self._pilFrames["stacked"] = PIL.ImageTk.PhotoImage(image=stacked)
        self._appCanvas["stacked"].create_image(0, 10, image=self._pilFrames["stacked"], anchor=tkinter.NW)

        # Add the layered image to the canvas
        self._pilFrames["layered"] = PIL.ImageTk.PhotoImage(image=layered)
        self._appCanvas["layered"].create_image(0, 225, image=self._pilFrames["layered"], anchor=tkinter.NW)

        frame = self._system[self._appString["device"].get()].original()["curr"]
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        # rgbFrame = cv2.
        imgFrame = PIL.Image.fromarray(cv2.resize(rgbFrame, (400, 400)))
        self._pilFrames["control"] = PIL.ImageTk.PhotoImage(image=imgFrame)
        self._appCanvas["control"].create_image(0, 225, image=self._pilFrames["control"], anchor=tkinter.NW)

        self.after(15, self.update)
