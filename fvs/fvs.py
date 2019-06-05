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

    def readFrame(self, *indices):
        return self.devices[indices[0]].readFrame() if len(indices) == 1 else [self.devices[camindx].readFrame() for camindx in indices]

class FoveatedDevice:
    def __init__(self, camindx):
        self.camindx = camindx
        self.vidcapt = cv2.VideoCapture(camindx)
        self.myframe = {"currimg": None, "previmg": None}
        self.myframe["previmg"] = self.vidcapt.read()[1]
        self.myframe["currimg"] = self.vidcapt.read()[1]
        self.myframe["previmg"] = utils.cropSquare(self.myframe["previmg"])
        self.myframe["currimg"] = utils.cropSquare(self.myframe["currimg"])
        self.focalpt = (-1000, -1000)
        self.visions = {}

    def addVision(self, visname, myratio, mypixls, *mytasks):
        self.visions[visname] = Vision(myratio, mypixls, mytasks, self.focalpt)
        return self.visions[visname]

    def getVision(self):
        return self.visions

    def addTask(self, visname, vistask):
        self.visions[visname].addTask(vistask)

    def readFrame(self):
        self.myframe["previmg"] = self.myframe["currimg"]
        self.myframe["currimg"] = utils.cropSquare(self.vidcapt.read()[1])
        [self.visions[visname].readFrame(self.myframe["currimg"], self.myframe["previmg"]) for visname in self.visions.keys()]
        return self.myframe["currimg"]

class Vision:
    def __init__(self, myratio, mypixls, mytasks, focalpt):
        self.myratio = myratio
        self.mypixls = mypixls
        self.mytasks = list(mytasks)
        self.focalpt = focalpt
        self.myframe = {}
        self.network = {}

    def readFrame(self, currimg, previmg):
        self.myframe["previmg"], self.myframe["currimg"] = [utils.cropRatio(image, self.myratio, self.focalpt) for image in [previmg, currimg]]
        self.myframe["previmg"], self.myframe["currimg"] = [utils.resizeImg(self.myframe[frame], self.mypixls) for frame in ["previmg", "currimg"]]
        [getattr(self, "get" + task.lower().capitalize())() for task in self.mytasks if task not in ["previmg", "currimg"]]

    def addTask(self, vistask):
        self.mytasks.append(vistask)
