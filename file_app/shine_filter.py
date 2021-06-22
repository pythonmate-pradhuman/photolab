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

kelvin_table = {
    1000: (255, 56, 0),
    1500: (255, 109, 0),
    2000: (255, 137, 18),
    2500: (255, 161, 72),
    3000: (255, 180, 107),
    3500: (255, 196, 137),
    4000: (255, 209, 163),
    4500: (255, 219, 186),
    5000: (255, 228, 206),
    5500: (255, 236, 224),
    6000: (255, 243, 239),
    6500: (255, 249, 253),
    7000: (245, 243, 255),
    7500: (235, 238, 255),
    8000: (227, 233, 255),
    8500: (220, 229, 255),
    9000: (214, 225, 255),
    9500: (208, 222, 255),
    10000: (204, 219, 255)}


def resize_shine(img, dim):
    col, row = dim
    img_ratio = img.shape[0] / img.shape[1]
    new_ratio = row / col
    new_img = np.zeros((row, col, 3)).astype(np.uint8)
    if img_ratio < new_ratio:
        img = imutils.resize(img, height=row)

        offset = int((img.shape[1] - col) / 2)
        new_img[:, :, :] = img[:, offset:col + offset, :]
    if img_ratio >= new_ratio:
        img = imutils.resize(img, width=col)
        offset = int((img.shape[0] - row) / 2)
        new_img[:, :, :] = img[offset:row + offset, :, :]

    return new_img


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


def convert_temp(img, temp):
    img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    r, g, b = kelvin_table[temp]
    matrix = (r / 255.0, 0.0, 0.0, 0.0,
              0.0, g / 255.0, 0.0, 0.0,
              0.0, 0.0, b / 255.0, 0.0)
    return cv2.cvtColor(np.asarray(img.convert('RGB', matrix)), cv2.COLOR_RGB2BGR)


def shine_filter(img,back_black,back_shine):
    main_img = img.copy()
    print('main_img.shape', main_img.shape)
    # try:
    #     print(os.path.join(os.path.abspath(os.path.join(
    #         instance.file.path, os.pardir))))
    # back_black = cv2.imread(os.path.join(os.path.abspath(os.path.join(
    #     instance.file.path, os.pardir)), "black-face-back.png"), -1)
    # back_shine = cv2.imread(os.path.join(os.path.abspath(
    #     os.path.join(instance.file.path, os.pardir)), "sun-shine-back.png"), -1)
    main_img = resize_shine(main_img, (540, 540))
    main_img = apply_brightness_contrast(
        main_img.copy(), brightness=-60, contrast=38)
    main_img = convert_temp(main_img, 10000)
    a = np.zeros((540, 540, 1)).astype(np.uint8)
    a[:, :, :] = 255
    main_img = np.concatenate((main_img, a), axis=2)
    back_black[:, :, 3] = back_black[:, :, 3] * 0.1
    back_shine[:, :, 3] = back_shine[:, :, 3] * 0.6

    main_img = Image.fromarray(main_img)
    back_black = Image.fromarray(back_black)
    back_shine = Image.fromarray(back_shine)

    main_img.paste(back_black, (0, 0), back_black)
    main_img.paste(back_shine, (0, 0), back_shine)

    main_img = np.array(main_img)
    return main_img
