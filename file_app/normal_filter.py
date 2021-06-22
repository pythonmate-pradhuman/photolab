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


def normal_filter(img, img2, img5):
    scale = 70
    width = int(img.shape[0] * scale / 100)
    height = int(img.shape[1] * scale / 100)
    img1 = cv2.resize(img, (width, height))
    # img2 = cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path,os.pardir)), "pic25.png"))

    img2 = cv2.bitwise_not(img2)
    scale_fac = 50
    w = img1.shape[0]
    h = img1.shape[1]

    x = 0
    y = int(img1.shape[1] * scale_fac / 100)
    # crop image accor
    img3 = img1[x:w, y:h]
    img4 = cv2.resize(img2, img3.shape[1::-1])
    #img4 = cv2.resize(img2, (img3.shape[0], img3.shape[1]))
    dst1 = cv2.bitwise_or(img3, img4)

    dst1[np.where((dst1 == [255, 255, 255]).all(axis=2))] = [211, 211, 211]

    # to place a pic at y
    rows, cols, channels = dst1.shape

    roi1 = dst1[0:rows, 0:cols]
    img1[0:w, y:y + cols] = roi1
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    (thresh, blawh) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    blur = cv2.GaussianBlur(blawh, (37, 37), 0)
    sum1 = cv2.addWeighted(blur, 0.3, gray, 0.9, 0)

    # providing effect
    # img5 = cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path,os.pardir)), "back.jpg"))
    img5 = cv2.resize(img5, img1.shape[1::-1])
    gray1 = cv2.cvtColor(img5, cv2.COLOR_BGR2GRAY)

    img = cv2.addWeighted(sum1, 0.9, gray1, 1, 0)
    img = cv2.resize(img, img.shape[1::-1])
    return img
