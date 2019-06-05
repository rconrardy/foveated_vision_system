import fvs

myfvs = fvs.FoveatedVisionSystem(0)

myfvs.addVision("mainfoveal", 1/3, 200, "currimg")
myfvs.addVision("parafoveal", 2/3, 200, "currimg")
myfvs.addVision("peripheral", 3/3, 200)

myfvs.addTasks("peripheral", "currimg")
net = myfvs.addNetwork(
    "C:\\Users\\conra\\Documents\\foveated_vision_system\\fvs\\dnn\\MobileNetSSD_deploy.prototxt.txt",
    "C:\\Users\\conra\\Documents\\foveated_vision_system\\fvs\\dnn\\MobileNetSSD_deploy.caffemodel"
)
print(net)

while True:
    if fvs.stopSignal():
        break
    cam0 = myfvs.readFrame(0)
    vis0 = myfvs.getVision(0)
    print(vis0["peripheral"].mytasks)
    fvs.showImage("original", cam0)
    fvs.showImage("mainfoveal", vis0["mainfoveal"].myframe["currimg"])
    fvs.showImage("parafoveal", vis0["parafoveal"].myframe["currimg"])
    fvs.showImage("peripheral", vis0["peripheral"].myframe["currimg"])
