import cv2
import human_parsing2.human_parser as human_parser
import imutils
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

def resize_even(img, max_dim):
    new_img = img.copy()
    if new_img.shape[0] > max_dim:
        new_img = imutils.resize(new_img, height=max_dim)
    if new_img.shape[1] > max_dim:
        new_img = imutils.resize(new_img, width=max_dim)
    return new_img


def draw_outline(mask):
    mask = mask.astype(np.uint8)
    img4 = np.zeros((mask.shape[0], mask.shape[1], 3)).astype(np.uint8)
    img4[:,:,0] = mask.copy()
    img4[:,:,1] = mask.copy()
    img4[:,:,2] = mask.copy()
    #img3.shape = (img3.shape[1], img3.shape[2], img3.shape[0])

    print(img4.shape, mask.shape)


    new_mask = cv2.Canny(img4, 1, 200)
    kernel = np.ones((4,4), np.uint8) 
    new_mask = cv2.dilate(new_mask,kernel,iterations = 1)

    ret, thresh = cv2.threshold(new_mask, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    new_mask = new_mask.astype(np.uint8)
    cv2.drawContours(new_mask, contours, -1, (255,255,255), 20)
    return new_mask

def apply(img,news,words):
    # news = cv2.imread("./news.jpeg")
    # words = cv2.imread("./words.jpeg")
    img = resize_even(img, 1080)
    news = cv2.resize(news, (img.shape[1], img.shape[0]))
    words = cv2.resize(words, (img.shape[1], img.shape[0]))
    # Making the image size small to get computation faster
    img_small = imutils.resize(img, width=500, inter=cv2.INTER_CUBIC)

    # Using the sengmentation parser on smaller image to get mask
    mask = human_parser.parse(img_small)

    # Making the mask bigger to match the original image size
    mask_big = cv2.resize(mask.astype(np.uint8), (img.shape[1], img.shape[0]))
    
    img1 = mask_big.copy()
    img1[img1!=0]=255
    img5 = img1.copy()
    new_mask = draw_outline(img5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img[:,:,0] = gray
    img[:,:,1] = gray
    img[:,:,2] = gray

    img4 = np.zeros((new_mask.shape[0], new_mask.shape[1], 3)).astype(np.uint8)
    img4[:,:,0] = new_mask
    img4[:,:,1] = new_mask
    img4[:,:,2] = new_mask

    img4[new_mask==0] = news[new_mask==0]
    img4[mask_big!=0] = img[mask_big!=0] 
    img4[np.isin(mask_big, [1,5,7])] = words[np.isin(mask_big, [1,5,7])]


    return img4
