import fvs

"""Make fvs and fps"""
myfvs = fvs.FoveatedVisionSystem(0)
myfps = fvs.fps()

"""Make visions"""
myfvs.addVision("mainfoveal", 1/4, 200)
myfvs.addVision("parafoveal", 2/4, 200)
myfvs.addVision("perifoveal", 3/4, 200)
myfvs.addVision("peripheral", 4/4, 200)

"""Caffe for object detection"""
# prototxt = "MobileNetSSD_deploy.prototxt.txt"
# dnnmodel = "MobileNetSSD_deploy.caffemodel"
# scale_factor =  0.007843
# size = (300, 300)
# mean = (127.5, 127.5, 127.5)
# classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
# confidence = 0.7
# myfvs.addTask("detectobjects", "caffe", "peripheral", ("curr", prototxt, dnnmodel, scale_factor, size, mean, classes, confidence))

"""Caffe for face detection"""
prototxt = "FaceNetSSD_deploy.prototxt.txt"
dnnmodel = "FaceNetSSD_deploy.caffemodel"
scale_factor =  1.0
size = (100, 100)
mean = (104.0, 177.0, 123.0)
classes = ["background", "face"]
confidence = 0.5
myfvs.addTask("detectfaces", "caffe", "peripheral", ("curr", prototxt, dnnmodel, scale_factor, size, mean, classes, confidence))

"""Haar face and eye detection"""
# myfvs.addTask("haarimage", "haar", "peripheral", ("curr"))

"""Do other tasks"""
myfvs.addTask("diffimage", "difference", "parafoveal", ("curr", "prev"))


myfps.start()
while True:
    if fvs.stopSignal():
        break

    myfvs.updateFrames()
    myfps.update()


    myfvs.showFrame(0, "mainfoveal", "curr")
    myfvs.showFrame(0, "parafoveal", "curr")
    myfvs.showFrame(0, "perifoveal", "curr")
    myfvs.showFrame(0, "peripheral", "curr")
    myfvs.showFrame(0, "peripheral", "detectfaces")
    myfvs.showFrame(0, "parafoveal", "diffimage")
    print("FPS: {0:.3}".format(myfps.fps()))

# myfps.stop()
