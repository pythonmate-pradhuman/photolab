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
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect
from matplotlib import pyplot as plt
from PIL import Image


def resize_cartoon(img):
    img3 = img.copy()
    if img3.shape[0] > 540:
        img3 = cv2.resize(img3, (0, 0), fy=540 /
                          img3.shape[0], fx=540/img3.shape[0])
    if img3.shape[1] > 540:
        img3 = cv2.resize(img3, (0, 0), fx=540 /
                          img3.shape[1], fy=540/img3.shape[1])
    return img3


def cartoon_filter(img):
    img2 = resize_cartoon(img)
    img2 = toonify.toonify(img2.astype(int))
    # img2[:,:,0] = img2[:,:,0] + 40
    img2 = cv2.cvtColor(img2.astype(np.uint8), cv2.COLOR_BGR2HSV)
    img2 = cv2.cvtColor(img2.astype(np.uint8), cv2.COLOR_HSV2BGR)

    blur = cv2.blur(img2, (20, 20))

    img3 = cv2.resize(img2, (0, 0), fx=0.8, fy=0.8)

    offx = math.floor((img2.shape[0] - img3.shape[0])/2)
    offy = math.floor((img2.shape[1] - img3.shape[1])/2)
    final_img = blur.copy()
    final_img[offx:offx+img3.shape[0], offy:offy+img3.shape[1], :] = img3
    # final_img is a numpy array
    return final_img
