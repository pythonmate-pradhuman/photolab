import body_parsing.body_parser as body_parser
import numpy as np
from matplotlib import pyplot as plt
import PIL
from PIL import Image, ImageDraw
import cv2
import imutils

def red_blue(img):
    img = img[:,:,:3]
    parsed = body_parser.parse(img)
    png_img = img.copy()
    black_mask = parsed.copy()
    black_mask.shape = (black_mask.shape[0], black_mask.shape[1], 1)
    black_mask[black_mask!=0]=255

    red = png_img.copy()

    mask = black_mask.copy()
    mask[mask!=0]=1
    mask[mask==0]=-1
    red = cv2.cvtColor(red, cv2.COLOR_BGR2HLS)
    red[:,:,0] = 128
    red[:,:,2] = 255
    red = cv2.cvtColor(red, cv2.COLOR_HLS2RGB)
    red=red*mask
    red = np.concatenate((red, mask), axis=2)
    blue = png_img.copy()
    blue = cv2.cvtColor(blue, cv2.COLOR_BGR2HLS)
    blue[:,:,0] = 203
    blue[:,:,2] = 255
    blue = cv2.cvtColor(blue, cv2.COLOR_HLS2RGB)

    blue=blue*mask
    red = red[:,50:,:]
    blue = blue[:,:-50,:]
    blue_canvas = np.zeros((img.shape[0],img.shape[1],3))
    red_canvas = np.zeros((img.shape[0],img.shape[1],3))
    blue_canvas[:,:,:] = -1
    red_canvas[:,:,:] = -1
    red_canvas[:,0:red.shape[1],:]=red[:,:,:3]
    blue_canvas[:,50:blue.shape[1]+50,:]=blue[:,:,:3]

    canvas = np.zeros((img.shape[0],img.shape[1],3))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if blue_canvas[i,j,0]>0 and red_canvas[i,j,0]>0:
                canvas[i,j,:] = np.minimum(255,blue_canvas[i,j,:]*1 + red_canvas[i,j,:]*1)
            elif blue_canvas[i,j,0]>=0:
                canvas[i,j,:] = blue_canvas[i,j,:]
            elif red_canvas[i,j,0]>=0:
                canvas[i,j,:] = red_canvas[i,j,:]
    return canvas.astype(np.uint8)