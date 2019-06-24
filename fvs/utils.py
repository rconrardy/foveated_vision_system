import math
import cv2

def cropSquare(frame):
    """Crop a square from the input frame."""

    # Get the original frame's height, width, and channels
    width, height, channels = frame.shape

    # Variables to hold the begin and end coordinates
    crop_x = [0, width]
    crop_y = [0, height]

    # Check to see if image is not square and give new coordinates
    if width > height:
        crop_x[0] = (width - height) // 2
        crop_x[1] = crop_x[0] + height
    elif width < height:
        crop_y[0] = (height - width) // 2
        crop_y[1] = crop_y[0] + width

    # Return part of the original image to make a square
    return frame[crop_x[0]:crop_x[1], crop_y[0]:crop_y[1]]


def cropRatio(frame, ratio, pixels, focal_point):
    old_size = frame.shape
    crop_begin_x = (old_size[0] - math.floor(old_size[0]*ratio)) // 2
    crop_end_x = old_size[0] - crop_begin_x
    crop_length_x = crop_end_x - crop_begin_x
    crop_begin_y = (old_size[1] - math.floor(old_size[1]*ratio)) // 2
    crop_end_y = old_size[1] - crop_begin_y
    crop_length_y = crop_end_y - crop_begin_y
    crop_begin_x = crop_begin_x + focal_point[0] * (old_size[0] // pixels)
    crop_end_x = crop_end_x + focal_point[0] * (old_size[0] // pixels)
    crop_begin_y = crop_begin_y - focal_point[1] * (old_size[1] // pixels)
    crop_end_y = crop_end_y - focal_point[1] * (old_size[1] // pixels)
    if crop_begin_x <= 0:
        crop_begin_x = 0
        crop_end_x = crop_length_x
    if crop_begin_y <= 0:
        crop_begin_y = 0
        crop_end_y = crop_length_y
    if crop_end_x >= old_size[0]:
        crop_end_x = old_size[0]
        crop_begin_x = old_size[0] - crop_length_x
    if crop_end_y >= old_size[1]:
        crop_end_y = old_size[1]
        crop_begin_y = old_size[1] - crop_length_y
    return frame[crop_begin_y:crop_end_y, crop_begin_x:crop_end_x]

# TODO
# def cropRatio(frame, ratio, pixels, focalpoint):
#     width, height, channels = frame.shape
#
#     crop_x = [(width - math.floor(width*ratio)) // 2, width - (width - math.floor(width*ratio)) // 2]
#     crop_y = [(height - math.floor(height*ratio)) // 2, height - (height - math.floor(height*ratio)) // 2]


def resizeImgCV2(frame, pixels):
     return cv2.resize(frame, (pixels, pixels))

def stopSignal():
    return True if cv2.waitKey(1) & 0xFF == ord('q') else False
