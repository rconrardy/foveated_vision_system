import cv2

visions = {
    "mainfoveal": {"ratio": 1/3, "size": 100, "jobs": []},
    "parafoveal": {"ratio": 2/3, "size": 100, "jobs": []},
    "perifoveal": {"ratio": 3/4, "size": 100, "jobs": []},
    "peripheral": {"ratio": 3/3, "size": 100, "jobs": []}
}

networks = {
    "object": {
        "classes": ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"],
        "prototxt": "C:\\Users\\conra\\Documents\\foveated_vision_system\\fvs\\dnn\\MobileNetSSD_deploy.prototxt.txt",
        "model": "C:\\Users\\conra\\Documents\\foveated_vision_system\\fvs\\dnn\\MobileNetSSD_deploy.caffemodel",
        "confidence": 0.7
    }
}

cascades = {
    "face": cv2.CascadeClassifier('haarcascade_frontalface_default.xml'),
    "eye": cv2.CascadeClassifier('haarcascade_eye.xml')
}
