import PIL.Image, PIL.ImageTk
import tkinter
import cv2

class Application(tkinter.Tk):
    def __init__(self, fvs, *args, **kwargs):
        """Initialize the Application given FoveatedVisionSystem."""

        # Initialize the application as a tkinter object
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.configure(bg="lightgray", width=1000, height=800)
        self.resizable(width=False, height=False)

        # FoveatedVisionSystem to display in application
        self.fvs = fvs

        # Store the frames for the application
        self.app_frames = {}
        self.app_option = {}
        self.app_choice = {}
        self.app_string = {}
        self.app_tracer = {}
        self.app_canvas = {}
        self.pil_frames = {}

        self.app_string["device"] = tkinter.StringVar(self)
        self.app_choice["device"] = [choice[0] for choice in self.fvs]
        self.app_string["device"].set(self.app_choice["device"][0])

        self.app_string["vision"] = tkinter.StringVar(self)
        self.app_choice["vision"] = [choice[0] for choice in self.fvs[self.app_string["device"].get()]]
        self.app_string["vision"].set(self.app_choice["vision"][0])

        self.app_string["frame"] = tkinter.StringVar(self)
        self.app_choice["frame"] = [choice[0] for choice in self.fvs[self.app_string["device"].get()][self.app_string["vision"].get()]]
        self.app_string["frame"].set(self.app_choice["frame"][0])

        # Create the master frame for the application
        self.title("Foveated Vision System")

        # Split the master frame into two left (west) and right (east) segments
        self.app_frames["west"] = tkinter.Frame(self, width=400, height=800, bg="lightgray")
        self.app_frames["east"] = tkinter.Frame(self, borderwidth=2, relief="solid", width=600, height=800, bg="lightgray")
        self.app_frames["west"].pack(side="left", fill="both")
        self.app_frames["east"].pack(side="right", fill="both", expand=True)

        self.app_frames["northwest"] = tkinter.Frame(self.app_frames["west"], borderwidth=2, relief="solid", width=400, height=400, bg="lightgray")
        self.app_frames["southwest"] = tkinter.Frame(self.app_frames["west"], borderwidth=2, relief="solid", width=400, height=400, bg="lightgray")
        self.app_frames["northwest"].pack(side="top", fill="both")
        self.app_frames["southwest"].pack(side="bottom", fill="both", expand=True)

        # Set up drop down menu to choose device
        self.app_option["device"] = tkinter.OptionMenu(self.app_frames["east"], self.app_string["device"], *self.app_choice["device"])
        self.app_option["device"].config(width=93, background="lightgray")
        self.app_option["device"].pack(side="top")


        self.app_option["vision"] = tkinter.OptionMenu(self.app_frames["east"], self.app_string["vision"], *self.app_choice["vision"])
        self.app_option["vision"].config(width=93, background="lightgray")
        self.app_option["vision"].pack(side="top")

        self.app_option["frame"] = tkinter.OptionMenu(self.app_frames["east"], self.app_string["frame"], *self.app_choice["frame"])
        self.app_option["frame"].config(width=93, background="lightgray")
        self.app_option["frame"].pack(side="top")

        # Create the canvases to hold the video streams
        self.app_canvas["layered"] = tkinter.Canvas(self.app_frames["northwest"], width=400, height=400, bg="lightgray")
        self.app_canvas["stacked"] = tkinter.Canvas(self.app_frames["southwest"], width=200, height=400, scrollregion=(0,0,200,800), bg="lightgray")
        self.app_canvas["control"] = tkinter.Canvas(self.app_frames["east"], width=600, height=800, bg="lightgray")

        # Set up scroll bar to scroll through frames
        self.scrollbar = tkinter.Scrollbar(self.app_frames["southwest"], bg="lightgray", command=self.app_canvas["stacked"].yview)
        self.scrollbar.pack(side="right", fill="y")

        self.app_canvas["stacked"].config(yscrollcommand=self.scrollbar.set)
        self.app_canvas["stacked"].pack(side="left", fill="both", expand=True)
        self.app_canvas["layered"].pack(side="left", fill="both", expand=True)
        self.app_canvas["control"].pack(fill="both", expand=True)

        self.app_tracer["device"] = self.app_string["device"].trace('w', self.update_device)
        self.app_tracer["vision"] = self.app_string["vision"].trace('w', self.update_vision)

    def update(self):
        self.fvs.update()

        # Create the blank images
        layered = PIL.Image.new('RGBA', (400, 400))
        stacked = PIL.Image.new('RGBA', (200, 800))
        control = PIL.Image.new('RGBA', (600, 800))

        # Get the stack and layered images from the frames
        i = 0

        # Loop through the visions in a device
        for vision_key, vision in self.fvs[self.app_string["device"].get()]:

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
        img_frame = cv2.cvtColor(self.fvs[self.app_string["device"].get()][self.app_string["vision"].get()][self.app_string["frame"].get()], cv2.COLOR_BGR2RGBA)
        control = PIL.Image.fromarray(cv2.resize(img_frame, (600, 600)))
        self.pil_frames["control"] = PIL.ImageTk.PhotoImage(image=control)
        self.app_canvas["control"].create_image(0, 90, image=self.pil_frames["control"], anchor=tkinter.NW)

        # Continue to update
        self.after(15, self.update)

    def update_device(self, *args):
        self.app_choice["vision"] = [choice[0] for choice in self.fvs[self.app_string["device"].get()]]
        self.app_string["vision"].set(self.app_choice["vision"][0])
        menu = self.app_option["vision"]["menu"]
        menu.delete(0, "end")
        for string in self.app_choice["vision"]:
            menu.add_command(label=string, command=lambda value=string: self.app_string["vision"].set(value))

    def update_vision(self, *args):
        self.app_choice["frame"] = [choice[0] for choice in self.fvs[self.app_string["device"].get()][self.app_string["vision"].get()]]
        self.app_string["frame"].set(self.app_choice["frame"][0])
        menu = self.app_option["frame"]["menu"]
        menu.delete(0, "end")
        for string in self.app_choice["frame"]:
            menu.add_command(label=string, command=lambda value=string: self.app_string["frame"].set(value))
