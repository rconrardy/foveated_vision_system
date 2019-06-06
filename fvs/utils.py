import cv2

def stopSignal():
    return True if cv2.waitKey(1) & 0xFF == ord('q') else False

def showImage(name, frame):
    cv2.imshow(name, frame)
