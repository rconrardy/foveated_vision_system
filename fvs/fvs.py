import fvs.config as config
import fvs.utils as utils
import numpy
import copy
import math
import cv2

class FoveatedVisionSystem:
    def __init__(self, *indices):
        self.devices = {camindx: FoveatedDevice(camindx) for camindx in indices}

    def addVision(self, visname, myratio, mypixls, *mytasks):
        return [self.devices[camindx].addVision(visname, myratio, mypixls, *mytasks) for camindx in self.devices.keys()]

    def getVision(self, *indices):
        return self.devices[indices[0]].getVision() if len(indices) == 1 else [self.devices[camindx].getVision() for camindx in indices]

    def addTasks(self, visname, *vistask, ):
        return [[self.devices[camindx].addTask(visname, task) for camindx in self.devices.keys()] for task in vistask]

    def addNetwork(self, prototxt, model):
        network = cv2.dnn.readNetFromCaffe(prototxt, model)
        return network

    def addDetect(self, protoxt, model):
        

    def readFrame(self, *indices):
        return self.devices[indices[0]].readFrame() if len(indices) == 1 else [self.devices[camindx].readFrame() for camindx in indices]

class FoveatedDevice:
    def __init__(self, camindx):
        self.camindx = camindx
        self.vidcapt = cv2.VideoCapture(camindx)
        self.myframe = {"curr": None, "prev": None}
        self.myframe["prev"] = self.vidcapt.read()[1]
        self.myframe["curr"] = self.vidcapt.read()[1]
        self.myframe["prev"] = utils.cropSquare(self.myframe["prev"])
        self.myframe["curr"] = utils.cropSquare(self.myframe["curr"])
        self.focalpt = (0, 0)
        self.visions = {}

    def addVision(self, visname, myratio, mypixls, *mytasks):
        self.visions[visname] = Vision(myratio, mypixls, mytasks, self.focalpt)
        return self.visions[visname]

    def getVision(self):
        return self.visions

    def addTask(self, visname, vistask):
        self.visions[visname].addTask(vistask)

    def readFrame(self):
        self.myframe["prev"] = self.myframe["curr"]
        self.myframe["curr"] = utils.cropSquare(self.vidcapt.read()[1])
        [self.visions[visname].readFrame(self.myframe["curr"], self.myframe["prev"]) for visname in self.visions.keys()]
        return self.myframe["curr"]

class Vision:
    def __init__(self, myratio, mypixls, mytasks, focalpt):
        self.myratio = myratio
        self.mypixls = mypixls
        self.mytasks = list(mytasks)
        self.focalpt = focalpt
        self.myframe = {}
        self.network = {}

    def readFrame(self, currimg, previmg):
        self.myframe["prev"], self.myframe["curr"] = [utils.cropRatio(image, self.myratio, self.focalpt) for image in [previmg, currimg]]
        self.myframe["prev"], self.myframe["curr"] = [utils.resizeImg(self.myframe[frame], self.mypixls) for frame in ["prev", "curr"]]
        [getattr(self, "get" + task.lower().capitalize())() for task in self.mytasks if task not in ["prev", "curr"]]

    def addTask(self, vistask):
        self.mytasks.append(vistask)

    def getGray(self):
        self.myframe["gray"] = cv2.cvtColor(self.myframe["curr"], cv2.COLOR_BGR2GRAY)

    def getLog(self):
        newsize = (self.myframe["curr"].shape[0]/2, self.myframe["curr"].shape[1]/2)
        self.myframe["log"] = cv2.logPolar(self.myframe["curr"], newsize, 40, cv2.WARP_FILL_OUTLIERS)

    def getLinear(self):
        newsize = (self.myframe["curr"].shape[0]/2, self.myframe["curr"].shape[1]/2,)
        self.myframe["linear"] = cv2.linearPolar(self.myframe["curr"], newsize, 40, cv2.WARP_FILL_OUTLIERS)
