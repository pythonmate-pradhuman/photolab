import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance
import cv2
import imutils
import human_parsing2.human_parser as human_parser
import numpy as np


def imshow(img):
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # Helper Function


def resize_cartoon(img):
    img3 = img.copy()
    if img3.shape[0] > 540:
        img3 = cv2.resize(img3, (0, 0), fy=540 /
                          img3.shape[0], fx=540/img3.shape[0])
    if img3.shape[1] > 540:
        img3 = cv2.resize(img3, (0, 0), fx=540 /
                          img3.shape[1], fy=540/img3.shape[1])
    return img3


def enhance(img):
    mask = img[:, :, 3:4]
    img2 = img.copy()
    img2 = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

    contrast = ImageEnhance.Contrast(img2)
    img2 = contrast.enhance(2)
    bright = ImageEnhance.Brightness(img2)
    img2 = bright.enhance(0.8)
    img2 = np.array(img2)
    return cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)


def resize_shine2(img, dim):
    row, col = dim[:2]
    img_ratio = img.shape[0]/img.shape[1]
    new_ratio = row/col
    new_img = np.zeros((row, col, img.shape[2])).astype(np.uint8)
    if img_ratio < new_ratio:
        img = imutils.resize(img, height=row)

        offset = int((img.shape[1] - col)/2)
        new_img[:, :, :] = img[:, offset:col+offset, :]
    if img_ratio >= new_ratio:
        img = imutils.resize(img, width=col)
        offset = int((img.shape[0] - row)/2)
        new_img[:, :, :] = img[offset:row+offset, :, :]
    plt.imshow(new_img)
    return new_img


def triple_exposer(img1, img2, img3):

    te1 = resize_cartoon(img1)

    te2 = resize_shine2(img2, te1.shape)

    te3 = resize_shine2(img3, te1.shape)

    img_small = imutils.resize(te1, width=500, inter=cv2.INTER_CUBIC)

    # Using the sengmentation parser on smaller image to get mask
    mask = human_parser.parse(img_small)

    # Making the mask bigger to match the original image size
    parsed = cv2.resize(mask.astype(np.uint8), (te1.shape[1], te1.shape[0]))

    te1 = enhance(te1)

    img1 = cv2.addWeighted(te2, 0.7, te3, 0.4, 0)
    img2 = cv2.addWeighted(te1, 1, img1, 0.4, 0)

    img1[parsed != 0] = img2[parsed != 0]
    final = img1  # Just to follow the same returning pattern

    return final
