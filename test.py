import fvs

myfvs = fvs.FoveatedVisionSystem(0)

myfvs.addVision("mainfoveal", 1/3, 400)
myfvs.addVision("mainparafoveal", 1.5/3, 400)
myfvs.addVision("parafoveal", 2/3, 150)
myfvs.addVision("mainparafoveal", 2.5/3, 400)
myfvs.addVision("peripheral", 3/3, 200)

prototxt = "MobileNetSSD_deploy.prototxt.txt"
dnnmodel = "MobileNetSSD_deploy.caffemodel"
scale_factor =  0.007843
size = (300, 300)
mean = (127.5, 127.5, 127.5)
classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
confidence = 0.7

myfvs.addTask("detectobjects", "caffe", "peripheral", ("curr", prototxt, dnnmodel, scale_factor, size, mean, classes, confidence))

myfvs.addTask("diffimage", "difference", "mainfoveal", ("curr", "prev"))
myfvs.addTask("grayimage", "gray", "mainfoveal", ("diffimage"))
myfvs.addTask("haarimage", "haar", "peripheral", ("curr"))

prototxt = "FaceNetSSD_deploy.prototxt.txt"
dnnmodel = "FaceNetSSD_deploy.caffemodel"
scale_factor =  1.0
size = (300, 300)
mean = (104.0, 177.0, 123.0)
classes = ["background", "face"]
confidence = 0.7

myfvs.addTask("detectfaces", "caffe", "peripheral", ("curr", prototxt, dnnmodel, scale_factor, size, mean, classes, confidence))

while True:
    if fvs.stopSignal():
        break

    myfvs.updateFrames()
    myfvs.showFrame(0, "mainfoveal", "curr")
    myfvs.showFrame(0, "mainparafoveal", "curr")
    myfvs.showFrame(0, "parafoveal", "curr")
    myfvs.showFrame(0, "mainfoveal", "diffimage")
    myfvs.showFrame(0, "mainfoveal", "grayimage")
    myfvs.showFrame(0, "peripheral", "detectobjects")
    myfvs.showFrame(0, "peripheral", "detectfaces")
    myfvs.showFrame(0, "peripheral", "haarimage")
