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


def filter_motivation(img, img4):
    # img=cv2.imread("moti4.jpg",-1)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    dim = (img.shape[1], img.shape[0])
    # resize image
    img4 = cv2.resize(img4, dim, interpolation=cv2.INTER_AREA)
    # added_image = cv2.addWeighted(img3,0.4,img,0.1,0)
    gw, gh, gc = img4.shape
    x = 0
    y = 0
    for i in range(0, gw):
        for j in range(0, gh):
            if img4[i, j][3] != 0:
                img[y + i, x + j] = img4[i, j]

    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img
