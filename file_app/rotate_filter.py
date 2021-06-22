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


def rotate_image(img, angle):
    dig_len = int(math.sqrt(img.shape[0] ** 2 + img.shape[1] ** 2))
    print("dig_len", dig_len)
    new_img = np.zeros((dig_len, dig_len, 4), np.uint8)
    diff_x = dig_len - img.shape[1]
    diff_y = dig_len - img.shape[0]
    print("dif_x", diff_x)
    new_img[int(diff_y / 2):img.shape[0] + int(diff_y / 2),
            int(diff_x / 2):img.shape[1] + int(diff_x / 2), :] = img
    img = new_img
    height, width = (img.shape[0], img.shape[1])
    size = (width, height)
    center = (width / 2, height / 2)
    dst_mat = np.zeros((height, width, 4), np.uint8)
    scale = 1
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    img_dst = cv2.warpAffine(img, rotation_matrix, size, dst_mat, flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_TRANSPARENT)
    return img_dst


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


def overlay_transparent(back, over, x, y):
    background = back.copy()
    overlay = over.copy()
    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1],
                         1), dtype=overlay.dtype) * 255
            ],
            axis=2,
        )

    # overlay_image = overlay[..., :3] if background.shape[2] < 4 else overlay[..., :]
    overlay_image = overlay[..., :3]
    # overlay_image = overlay[0:(overlay.shape[0] if overlay.shape[0]>y+h else overlay.shape[0]-h), 0:(overlay.shape[1] if overlay.shape[1]>x+w
    mask = overlay[..., 3:] / 255.0

    # y2 = (back.shape[0] if back.shape[0]>(y+h) else y+h)

    # x2 = (back.shape[1] if back.shape[1]>(x+w) else x+w)

    if background.shape[2] < 4:
        background[y:y + h, x:x + w] = (1.0 - mask) * \
            background[y:y + h, x:x + w] + mask * overlay_image
    else:
        background[y:y + h, x:x + w, :3] = (1.0 - mask) * \
            background[y:y + h, x:x + w, :3] + mask * overlay_image
        m = mask * 255
        print(m.shape)
        background[y:y + h, x:x + w, 3] = np.reshape(m, m.shape[0:2])
    # new_back = back.copy()
    return background


def filter(image, instance):
    print('filterfunction', image.shape)
    background0 = np.zeros((540, 540, 3)).astype(np.uint8)
    background0[:, :, :] = 255
    fourth_ch = np.zeros(background0.shape[0:2])
    fourth_ch[:, :] = 255
    fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
    background = background0
    print("#######################################################################")
    if (image.shape[0] < image.shape[1]):
        print("hdbcdvcgdvgcvgbc")
        try:
            backhori = cv2.imread(os.path.join(os.path.abspath(
                os.path.join(instance.file.path, os.pardir)), "back_hori.png"), -1)
        except:
            backhori = cv2.imread(os.path.join(os.path.abspath(
                os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]),-1)            
        backhori = imutils.resize(backhori, height=540, width=540)
        cv2.imwrite('test.jpg', backhori)
        presketch = resize_shine(image, (309, 235))
        presketch = cv2.cvtColor(presketch, cv2.COLOR_RGB2GRAY)

        image = resize_shine(image, (222, 164))
        # presketch = imutils.resize(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), height=470)
        fourth_ch = np.zeros(image.shape[0:2])
        fourth_ch[:, :] = 255
        fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
        image = np.concatenate((image, fourth_ch), axis=2)
        sketch = np.stack((presketch,) * 3, axis=-1)
        fourth_ch = np.zeros(sketch.shape[0:2])
        fourth_ch[:, :] = 255
        fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
        sketch = np.concatenate((sketch, fourth_ch), axis=2)
        image = rotate_image(image, 14)
        sketch = rotate_image(sketch, 346)
        background = overlay_transparent(background, sketch, 146, 51)
        background = overlay_transparent(background, image, 15, 210)
        print("hbxhzbhbxhzb")
        final = overlay_transparent(background, backhori, 0, 0)

    elif (image.shape[0] > image.shape[1]):
        print("sdfghnm,mngfdscvbnjygfcgvhbjhvghubvbhub huhb hnhjb hnjn")
        try:
            backverti = cv2.imread(os.path.join(os.path.abspath(
                os.path.join(instance.file.path, os.pardir)), "back_verti.png"), -1)
        except:
            backverti = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]), -1)
        backverti = imutils.resize(backverti, height=540, width=540)
        presketch = resize_shine(image, (264, 345))
        presketch = cv2.cvtColor(presketch, cv2.COLOR_RGB2GRAY)

        image = resize_shine(image, (172, 232))
        fourth_ch = np.zeros(image.shape[0:2])
        fourth_ch[:, :] = 255
        fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
        image = np.concatenate((image, fourth_ch), axis=2)
        sketch = np.stack((presketch,) * 3, axis=-1)
        fourth_ch = np.zeros(sketch.shape[0:2])
        fourth_ch[:, :] = 255
        fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
        sketch = np.concatenate((sketch, fourth_ch), axis=2)
        image = rotate_image(image, 14)
        sketch = rotate_image(sketch, 348)
        background = overlay_transparent(background, sketch, 106, 35)
        background = overlay_transparent(background, image, 0, 195)
        print("bhsvgvxzhbchxbj")
        final = overlay_transparent(background, backverti, 0, 0)
    return final
