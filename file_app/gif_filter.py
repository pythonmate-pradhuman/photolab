import io
import json
import math
import os

import cartoonize.toonify as toonify
import cv2
import cv2 as cv
import imageio
import imutils
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


def gif_filter(img):
    image = img
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([99, 50, 30])
    upper_red = np.array([200, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask3 = np.zeros_like(image)
    mask3[:, :, 0] = mask
    mask3[:, :, 1] = mask
    mask3[:, :, 2] = mask
    blue = cv2.bitwise_and(image, mask3)
    red = cv2.cvtColor(blue, cv2.COLOR_BGR2RGB)
    b, g, r = cv2.split(red)
    green = cv2.merge([g, r, b])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    gray = cv2.bitwise_and(img, 255 - mask3)
    bluefinal = gray + blue
    redfinal = gray + red
    greenfinal = gray + green

    img = [bluefinal, redfinal, greenfinal]  # here read all images
    return img
    # obj = io.BytesIO(b"")
    # imageio.mimsave(obj, img, 'GIF', duration=0.2)
    # # Example use ----------------------
    # f2 = open('./media/files/output'+ str(instance.id) +'.gif', "wb+")
    # processed_image = request.scheme + "://" + request.META["HTTP_HOST"] + "/media/files/output" + str(instance.id) + ".gif"
    # f2.write(obj.getvalue())
