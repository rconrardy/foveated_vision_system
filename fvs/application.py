import PIL.Image, PIL.ImageTk
import tkinter
import cv2

class Application(tkinter.Tk):
    def __init__(self, system, *args, **kwargs):
        """Initialize the Application given a system."""

        # Initialize the application as a tkinter.Tk object
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Foveated Vision System")
        self.configure(bg="lightgray", width=1200, height=800)
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

        # Split the master frame into two left (west) and right (east) segments
        self._appFrames["west"] = tkinter.Frame(self, width=400, height=800, bg="lightgray")
        self._appFrames["east"] = tkinter.Frame(self, borderwidth=2, relief="solid", width=600, height=800, bg="lightgray")
        self._appFrames["west"].pack(side="left", fill="both")
        self._appFrames["east"].pack(side="right", fill="both", expand=True)

        # Split the west frame into two top (northwest) and bottom (southwest) segments
        self._appFrames["northwest"] = tkinter.Frame(self._appFrames["west"], borderwidth=2, relief="solid", width=400, height=400, bg="lightgray")
        self._appFrames["southwest"] = tkinter.Frame(self._appFrames["west"], borderwidth=2, relief="solid", width=400, height=400, bg="lightgray")
        self._appFrames["northwest"].pack(side="top", fill="both")
        self._appFrames["southwest"].pack(side="bottom", fill="both", expand=True)

        # Set up drop down menu to choose device
        self._appOption["device"] = tkinter.OptionMenu(self._appFrames["east"], self._appString["device"], *self._appChoice["device"])
        self._appOption["device"].config(width=125, background="lightgray")
        self._appOption["device"].pack(side="top")

        # Set up drop down menu to choose vision
        self._appOption["vision"] = tkinter.OptionMenu(self._appFrames["east"], self._appString["vision"], *self._appChoice["vision"])
        self._appOption["vision"].config(width=125, background="lightgray")
        self._appOption["vision"].pack(side="top")

        # Set up drop down menu to choose frame
        self._appOption["frame"] = tkinter.OptionMenu(self._appFrames["east"], self._appString["frame"], *self._appChoice["frame"])
        self._appOption["frame"].config(width=125, background="lightgray")
        self._appOption["frame"].pack(side="top")

        # Create the canvases to hold the video streams
        self._appCanvas["layered"] = tkinter.Canvas(self._appFrames["northwest"], width=400, height=400, bg="lightgray")
        self._appCanvas["stacked"] = tkinter.Canvas(self._appFrames["southwest"], width=200, height=400, scrollregion=(0,0,200,800), bg="lightgray")
        self._appCanvas["control"] = tkinter.Canvas(self._appFrames["east"], width=600, height=800, bg="lightgray")

        # Set up scroll bar to scroll through frames
        self.scrollbar = tkinter.Scrollbar(self._appFrames["southwest"], bg="lightgray", command=self._appCanvas["stacked"].yview)
        self.scrollbar.pack(side="right", fill="y")

        # Display the images inside their respective frames
        self._appCanvas["stacked"].config(yscrollcommand=self.scrollbar.set)
        self._appCanvas["stacked"].pack(side="left", fill="both", expand=True)
        self._appCanvas["layered"].pack(side="left", fill="both", expand=True)
        self._appCanvas["control"].pack(fill="both", expand=True)

        # Create tracers to track changes in device or vision choice
        self._appTracer["device"] = self._appString["device"].trace('w', self.updateDevice)
        self._appTracer["vision"] = self._appString["vision"].trace('w', self.updateVision)

        # Tell the device to update itself
        self.update()

    def update(self):
        """Update the images that are displayed from the video stream."""

        # Update the vision frames in the system
        self._system.update()

        # Create blank PIL images to hold the video streams
        layered = PIL.Image.new('RGBA', (400, 400))
        stacked = PIL.Image.new('RGBA', (200, 800))
        control = PIL.Image.new('RGBA', (600, 800))

        # Get each vision key and vision for the selected device
        visionList = [(visionKey, vision) for visionKey, vision in self._system[self._appString["device"].get()]]

        # Loop through each vision in the vision list
        for i, (visionKey, vision) in enumerate(visionList):

            # Grab the frames from the vision when it is "curr"
            frameList = [frame for frameKey, frame in vision if frameKey=="curr"]

            # Loop through each frame in the frame list
            for frame in frameList:

                # Get the properties and turn the image into RGBA
                ratio, size = vision.properties()
                rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

                # Paste the images together in layered
                imgFrame = PIL.Image.fromarray(cv2.resize(rgbFrame, (int(400 * ratio), int(400 * ratio))))
                layered.paste(imgFrame, (int(200 * (1 - ratio)), int(200 * (1 - ratio))))

                # Paste the images together in stacked
                imgFrame = PIL.Image.fromarray(cv2.resize(rgbFrame, (200, 200)))
                stacked.paste(imgFrame, (0, 200 * i))

        # Add the stacked image to the canvas
        self._pilFrames["stacked"] = PIL.ImageTk.PhotoImage(image=stacked)
        self._appCanvas["stacked"].create_image(100, 0, image=self._pilFrames["stacked"], anchor=tkinter.NW)

        # Add the layered image to the canvas
        self._pilFrames["layered"] = PIL.ImageTk.PhotoImage(image=layered)
        self._appCanvas["layered"].create_image(0, 0, image=self._pilFrames["layered"], anchor=tkinter.NW)

        # Add the control image to the canvas
        imgFrame = cv2.cvtColor(self._system[self._appString["device"].get()][self._appString["vision"].get()][self._appString["frame"].get()], cv2.COLOR_BGR2RGBA)
        control = PIL.Image.fromarray(cv2.resize(imgFrame, (600, 600)))
        self._pilFrames["control"] = PIL.ImageTk.PhotoImage(image=control)
        self._appCanvas["control"].create_image(100, 90, image=self._pilFrames["control"], anchor=tkinter.NW)

        # Continue to update with a delay of 15
        self.after(15, self.update)

    def updateDevice(self, *args):
        """Update the vision choices when a new device is selected."""

        # Update the list of vision choices and the default vision choice
        self._appChoice["vision"] = [choice[0] for choice in self._system[self._appString["device"].get()]]
        self._appString["vision"].set(self._appChoice["vision"][0])

        # Delete the old choices fromt the option menu
        menu = self._appOption["vision"]["menu"]
        menu.delete(0, "end")

        # Add the new list of choices to the option menu
        for string in self._appChoice["vision"]:
            menu.add_command(label=string, command=lambda value=string: self._appString["vision"].set(value))

    def updateVision(self, *args):
        """Update the frame choices whena new vision is selected."""

        # Update the list of frame choices and the default frame choice
        self._appChoice["frame"] = [choice[0] for choice in self._system[self._appString["device"].get()][self._appString["vision"].get()]]
        self._appString["frame"].set(self._appChoice["frame"][0])

        # Delete the old choices fromt the option menu
        menu = self._appOption["frame"]["menu"]
        menu.delete(0, "end")

        # Add the new list of choices to the option menu
        for string in self._appChoice["frame"]:
            menu.add_command(label=string, command=lambda value=string: self._appString["frame"].set(value))
