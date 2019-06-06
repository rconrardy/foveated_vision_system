import fvs

myfvs = fvs.FoveatedVisionSystem(0)

myfvs.addVision("mainfoveal", 1/3, 200)
myfvs.addVision("parafoveal", 2/3, 200)
myfvs.addVision("peripheral", 3/3, 200)

print(myfvs.addTasks("peripheral", "gray", "log"))

prototxt = "C:\\Users\\conra\\Documents\\foveated_vision_system\\fvs\\dnn\\MobileNetSSD_deploy.prototxt.txt"
dnnmodel = "C:\\Users\\conra\\Documents\\foveated_vision_system\\fvs\\dnn\\MobileNetSSD_deploy.caffemodel"
net = myfvs.addNetwork(prototxt, dnnmodel)
myfvs.addDetect()

print(net)

while True:
    if fvs.stopSignal():
        break
    cam0 = myfvs.readFrame(0)
    vis0 = myfvs.getVision(0)
    print(vis0["peripheral"].mytasks)
    fvs.showImage("original", cam0)
    fvs.showImage("mainfoveal", vis0["mainfoveal"].myframe["curr"])
    fvs.showImage("parafoveal", vis0["parafoveal"].myframe["curr"])
    fvs.showImage("peripheral", vis0["peripheral"].myframe["gray"])
