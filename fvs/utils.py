import math
import cv2

def cropSquare(myframe):
    oldsize = myframe.shape
    crpbgnx = 0
    crpendx = oldsize[0]
    crpbgny = 0
    crpendy = oldsize[1]
    if crpendx > crpendy:
        crpendx = crpendy
    if crpendy > crpendx:
        crpendy = crpendx
    return myframe[crpbgnx:crpendx, crpbgny:crpendy]

def cropRatio(myframe, myratio, focalpt=(0,0)):
    oldsize = myframe.shape
    crpbgnx = (oldsize[0] - math.floor(oldsize[0]*myratio)) // 2
    crpendx = oldsize[0] - crpbgnx
    crplenx = crpendx - crpbgnx
    crpbgny = (oldsize[1] - math.floor(oldsize[1]*myratio)) // 2
    crpendy = oldsize[1] - crpbgny
    crpleny = crpendy - crpbgny
    crpbgnx = crpbgnx + focalpt[0]
    crpendx = crpendx + focalpt[0]
    crpbgny = crpbgny - focalpt[1]
    crpendy = crpendy - focalpt[1]
    if crpbgnx <= 0:
        crpbgnx = 0
        crpendx = crplenx
    if crpbgny <= 0:
        crpbgny = 0
        crpendy = crpleny
    if crpendx >= oldsize[0]:
        crpendx = oldsize[0]
        crpbgnx = oldsize[0] - crplenx
    if crpendy >= oldsize[1]:
        crpendy = oldsize[1]
        crpbgny = oldsize[1] - crpleny
    return myframe[crpbgny:crpendy, crpbgnx:crpendx]

def resizeImg(myframe, mypixls):
     return cv2.resize(myframe, (mypixls, mypixls))

def stopSignal():
    return True if cv2.waitKey(1) & 0xFF == ord('q') else False

def showImage(name, frame):
    cv2.imshow(name, frame)
