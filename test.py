import fvs

prototxt = "C:\\Users\\conra\\Documents\\foveated_vision_system\\fvs\\dnn\\MobileNetSSD_deploy.prototxt.txt"
dnnmodel = "C:\\Users\\conra\\Documents\\foveated_vision_system\\fvs\\dnn\\MobileNetSSD_deploy.caffemodel"
classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
confidence = 0.7

myfvs = fvs.FoveatedVisionSystem(0)

myfvs.addVision("mainfoveal", 1/3, 200)
myfvs.addVision("parafoveal", 2/3, 400)
myfvs.addVision("peripheral", 3/3, 600)

myfvs.addTask("linearimage", "linear", "parafoveal", ("curr"))
myfvs.addTask("detectobjects", "detection", "peripheral", ("curr", prototxt, dnnmodel, classes, confidence))


# myfvs.addTask("currgray", "gray", "parafoveal", ("curr"))
# myfvs.addTask("paradiff", "difference", "parafoveal", ("prev", "curr"))
#
# myfvs.addTask("linearimage", "linear", "peripheral", ("curr"))
# myfvs.addTask("linearimage", "linear", "mainfoveal", ("curr"))
# myfvs.addTask("prevedge", "edge", "peripheral", ("linearimage"))
#
# myfvs.addTask("grayimage1", "gray", "peripheral", ("linearimage"))
# myfvs.addTask("grayimage2", "gray", "peripheral", ("curr"))


while True:
    if fvs.stopSignal():
        break

    myfvs.updateFrames()

    myfvs.showFrame(0, "parafoveal", "curr")
    myfvs.showFrame(0, "mainfoveal", "curr")
    myfvs.showFrame(0, "peripheral", "detectobjects")
    # myfvs.showFrame(0, "peripheral", "prevedge")
    # myfvs.showFrame(0, "parafoveal", "paradiff")
    # myfvs.showFrame(0, "peripheral", "linearimage")
    # myfvs.showFrame(0, "mainfoveal", "linearimage")
