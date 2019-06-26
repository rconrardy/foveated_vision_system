import numpy
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


def cropRatio(frame, ratio, pixels, focalpoint):
    """Crop a new square from a frame given the desired ratio, pixels, and focalpoint."""

    # Get the original frame's height, width, and channels
    width, height, channels = frame.shape

    # Variables to hold the begin and end coordinates
    crop_x = [(width - math.floor(width*ratio)) // 2, width - (width - math.floor(width*ratio)) // 2]
    crop_y = [(height - math.floor(height*ratio)) // 2, height - (height - math.floor(height*ratio)) // 2]

    # Get the size of the frame
    size_x = crop_x[1] - crop_x[0]
    size_y = crop_y[1] - crop_y[0]

    # Get the size of the frame given the focalpoint offset
    # print(width, pixels)
    crop_x[0] += focalpoint[0] * (width // pixels)
    crop_x[1] += focalpoint[0] * (width // pixels)
    crop_y[0] -= focalpoint[1] * (height // pixels)
    crop_y[1] -= focalpoint[1] * (height // pixels)

    # Make sure that the new frame is inside the range on the x axis
    if crop_x[0] <= 0:
        crop_x[0] = 0
        crop_x[1] = size_x
    elif crop_x[1] > width:
        crop_x[0] = width - size_x
        crop_x[1] = width

    # Make sure that the new frame is inside the range on the y axis
    if crop_y[0] < 0:
        crop_y[0] = 0
        crop_y[1] = size_y
    elif crop_y[1] > height:
        crop_y[0] = height - size_y
        crop_y[1] = size_y

    # Return part of the original image
    return frame[crop_y[0]:crop_y[1], crop_x[0]:crop_x[1]]
