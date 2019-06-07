import fvs.config as config
import fvs.fvs_utils as utils
import numpy
import copy
import math
import cv2
import os

class FoveatedVisionSystem:
    def __init__(self, *camera_indices):
        """Initialize the FoveatedVisionSystem given multiple camera indices."""
        self.devices = {camera_index: FoveatedDevice(camera_index) for camera_index in camera_indices}

    def addDevice(camera_index):
        """Add a new FoveatedDevice given a camera index."""
        self.devices[camera_index] = FoveatedDevice(camera_index)

    def removeDevice(camera_index):
        """Remove a FoveatedDevice given a camera index."""
        del self.devices[camera_index]

    def getDevices(self):
        """Returns all FoveatedDevices contained in the FoveatedVisionSystem."""
        return self.devices

    def getDevice(self, camera_index):
        """Returns a FoveatedDevice given a camera index"""
        return self.getDevices()[camera_index]

    def addVision(self, vision_name, ratio, pixels):
        """Add a Vision given a vision name, ratio, and pixels."""
        [self.devices[camera_index].addVision(vision_name, ratio, pixels) for camera_index in self.devices.keys()]

    def removeVision(self, vision_name):
        """Remove a Vision given a vision name."""
        [self.devices[camera_index].removeVision(vision_name) for camera_index in self.devices.keys()]

    def getVisions(self, camera_index):
        """Returns all Visions in a FoveatedDevice given a camera index."""
        return self.devices[camera_index].visions

    def getVision(self, camera_index, vision_name):
        """Returns a single Vision from a FoveatedDevice given a camera index and vision name."""
        return self.getVisions(camera_index)[vision_name]

    def addTask(self, task_name, task_type, vision_name, args):
        """Add a task to a Vision given a task name, task type, vision name, and arguments for the function."""
        [self.devices[camera_index].addTask(task_name, task_type, vision_name, args) for camera_index in self.devices.keys()]

    def removeTask(self, task_name, vision_name):
        """Remove a task from a Vision given task name and vision name."""
        [self.devices[camera_index].removeTask(task_name, vision_name) for camera_index in self.devices.keys()]

    def getTasks(self, camera_index, vision_name):
        """Returns all tasks from a Visiom given a camera index and vision name."""
        return self.devices[camera_index].visions[vision_name].tasks

    def getTask(self, camera_index, vision_name, task_name):
        """Returns a task from Vision given a camera index, vision name, and task name."""
        return self.getTasks(camera_index, vision_name)[task_name]

    def updateFrames(self):
        """Updates the frames in all devices."""
        [self.devices[camera_index].updateFrames() for camera_index in self.devices.keys()]

    def getFrames(self, camera_index, vision_name):
        """Returns all vision frames given a camera index and vision name."""
        return self.devices[camera_index].visions[vision_name].frames

    def getFrame(self, camera_index, vision_name, frame_name):
        """Returns a signle frame given a camera index, vision name, and frame name."""
        return self.getFrames(camera_index, vision_name)[frame_name]

    def showFrame(self, camera_index, vision_name, frame_name):
        """Shows a single frame given the camera index, vision name, and frame name."""
        cv2.imshow(vision_name + frame_name, self.getFrame(camera_index, vision_name, frame_name))

class FoveatedDevice:
    def __init__(self, camera_index):
        """Initialize the FoveatedDevice given a camera index."""
        self.camera_index = camera_index
        self.video_capture = cv2.VideoCapture(camera_index)
        self.frames = {"curr": None, "prev": None}
        self.frames["prev"] = self.video_capture.read()[1]
        self.frames["curr"] = self.video_capture.read()[1]
        self.frames["prev"] = utils.cropSquare(self.frames["prev"])
        self.frames["curr"] = utils.cropSquare(self.frames["curr"])
        self.focal_point = [0, 0]
        self.visions = {}

    def addVision(self, vision_name, ratio, pixels):
        """Add a Vision to the FoveatedDevice given a vision name, ration, and pixels."""
        self.visions[vision_name] = Vision(ratio, pixels, self.focal_point)
        return self.visions[vision_name]

    def removeVision(self, vision_name):
        """Remove a Vision from the FoveatedDevice given a vision name."""
        del self.visions[vision_name]

    def addTask(self, task_name, task_type, vision_name, args):
        """Add a task to a Vision given a task name, task type, vision name, and arguments for the function."""
        self.visions[vision_name].addTask(task_name, task_type, args)

    def removeTask(self, task_name, vision_name):
        """Remove a task from a Vision given a task name and vision name."""
        self.visions[vision_name].removeTask(task_name)

    def updateFrames(self):
        """Updates the frames in the FoveatedDevice."""
        self.frames["prev"] = self.frames["curr"]
        self.frames["curr"] = utils.cropSquare(self.video_capture.read()[1])
        [self.visions[vision_name].updateFrames(self.frames["curr"], self.frames["prev"]) for vision_name in self.visions.keys()]
        return self.frames["curr"]

class Vision:
    def __init__(self, ratio, pixels, focal_point):
        """Initialize the Vision given a ratio, pixels, and focal point."""
        self.ratio = ratio
        self.pixels = pixels
        self.focal_point = focal_point
        self.frames = {}
        self.tasks = {}
        self.networks = {}

    def updateFrames(self, curr, prev):
        """Update all the frames in the Vision given the original curr and previous frames."""
        self.frames["prev"], self.frames["curr"] = [utils.cropRatio(image, self.ratio, self.pixels, self.focal_point) for image in [prev, curr]]
        self.frames["prev"], self.frames["curr"] = [utils.resizeImg(self.frames[frame], self.pixels) for frame in ["prev", "curr"]]
        [getattr(self, "get" + val[0].lower().capitalize())(key, val[1]) for key, val in self.tasks.items()]

    def addTask(self, task_name, task_type, args):
        """Add a task to the Vision given a task name, task type, and arguments for the function."""
        if task_type == "caffe":
            self.addNetwork(task_name, args[1], args[2], args[6])
        self.tasks[task_name] = (task_type, args)

    def removeTask(self, task_name):
        """Remove a task from the vision given a task name."""
        if self.tasks[task_name][0] == "caffe":
            self.removeNetwork(task_name)
        del self.tasks[task_name]

    def addNetwork(self, task_name, prototxt, model, classes):
        """Add a network to the Vision given a task name, prototxt, model, and classes."""
        mycolor = numpy.random.uniform(0, 255, size=(len(classes), 3))
        caffes = os.path.join(os.path.dirname(__file__), '')
        prototxt = caffes + "\\caffe\\" + prototxt
        model = caffes + "\\caffe\\" + model
        self.networks[task_name] = (cv2.dnn.readNetFromCaffe(prototxt, model), classes, mycolor)

    def removeNetwork(self, task_name):
        """Remove a network from the Vision given a task name."""
        del self.networks[task_name]

    def getGray(self, task_name, args):
        """Get a gray version of the current image."""
        self.frames[task_name] = cv2.cvtColor(self.frames[args], cv2.COLOR_BGR2GRAY)

    def getEdge(self, task_name, args):
        self.frames[task_name] = cv2.Canny(self.frames[args], 100, 200)

    def getDifference(self, task_name, args):
        abs_diff = cv2.absdiff(self.frames[args[0]], self.frames[args[1]])
        self.frames[task_name] = cv2.threshold(abs_diff, 30, 255, cv2.THRESH_BINARY)[1]

    def getLog(self, task_name, args):
        new_size = (self.frames[args].shape[0]/2, self.frames[args].shape[1]/2)
        self.frames[task_name] = cv2.logPolar(self.frames[args], new_size, 40, cv2.WARP_FILL_OUTLIERS)

    def getLinear(self, task_name, args):
        new_size = (self.frames[args].shape[0]/2, self.frames[args].shape[1]/2,)
        self.frames[task_name] = cv2.linearPolar(self.frames[args], new_size, 40, cv2.WARP_FILL_OUTLIERS)

    def getHaar(self, task_name, args):
        haarcascades = os.path.join(os.path.dirname(__file__), '')
        face_cascade = cv2.CascadeClassifier(haarcascades + "cascade\\haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier(haarcascades + "cascade\\haarcascade_eye.xml")
        self.frames[task_name] = copy.deepcopy(self.frames[args])
        gray_image = cv2.cvtColor(self.frames[task_name], cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
        for (x, y, w, h) in faces:
            self.frames[task_name] = cv2.rectangle(self.frames[task_name], (x,y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray_image[y:y+h, x:x+w]
            roi_color = self.frames[task_name][y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)


    def getCaffe(self, task_name, args):
        # blob = cv2.dnn.blobFromImage(cv2.resize(self.frames[args[0]], args[4]), args[3], args[4], args[5])
        blob = cv2.dnn.blobFromImage(cv2.resize(self.frames[args[0]], (self.pixels, self.pixels)), args[3], (self.pixels, self.pixels), args[5])
        self.networks[task_name][0].setInput(blob)
        detections = self.networks[task_name][0].forward()
        self.frames[task_name] = copy.deepcopy(self.frames[args[0]])
        (h, w) = self.frames[task_name].shape[:2]
        # print(h, w)
        for i in numpy.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > args[7]:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * numpy.array([w, h, w, h])
                (startx, starty, endx, endy) = box.astype("int")
                label = "{}: {:.2f}%".format(self.networks[task_name][1][idx], confidence * 100)
                cv2.rectangle(self.frames[task_name], (startx, starty), (endx, endy), self.networks[task_name][2][idx], 2)
                y = starty - 15 if starty - 15 > 15 else starty + 15
                cv2.putText(self.frames[task_name], label, (startx, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.networks[task_name][2][idx], 2)
                if self.networks[task_name][1][idx] == "face" or self.networks[task_name][1][idx] == "car":
                    self.focal_point[0] = (endx - (endx - startx)//2) - self.pixels//2
                    self.focal_point[1] = -(endy - (endy - starty)//2) + self.pixels//2
        print(self.focal_point)
