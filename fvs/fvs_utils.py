import math
import cv2

def cropSquare(frame):
    old_size = frame.shape
    crop_begin_x = 0
    crop_end_x = old_size[0]
    crop_begin_y = 0
    crop_end_y = old_size[1]
    if crop_end_x > crop_end_y:
        crop_end_x = crop_end_y
    if crop_end_y > crop_end_x:
        crop_end_y = crop_end_x
    return frame[crop_begin_x:crop_end_x, crop_begin_y:crop_end_y]

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

def resizeImg(frame, pixels):
     return cv2.resize(frame, (pixels, pixels))
