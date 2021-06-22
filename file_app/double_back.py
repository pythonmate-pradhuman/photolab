import numpy as np
import PIL
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw
import cv2
import imutils
import human_parsing2.human_parser as human_parser

def apply(main_image):
    
    main_img = main_image
    
    # Making the image size small to get computation faster
    img_small = imutils.resize(main_img, width=500, inter=cv2.INTER_CUBIC)

    # Using the sengmentation parser on smaller image to get mask
    mask = human_parser.parse(img_small)

    # Making the mask bigger to match the original image size
    body_parts = cv2.resize(mask.astype(np.uint8), (main_img.shape[1], main_img.shape[0]))#imutils.resize(mask.astype(float), height=img.shape[0], width=img.shape[1], inter=cv2.INTER_CUBIC)
    
    background=np.array(np.where(body_parts==0))
    body=np.array(np.where(body_parts!=0))
    bg1=cv2.imread("mountains.jpg")
    bg2=cv2.imread("buildings.jpg")
    bg1=cv2.resize(bg1,(main_img.shape[1],main_img.shape[0]))
    bg2=cv2.resize(bg2,(main_img.shape[1],main_img.shape[0]))
    main_img[list(background)]=bg1[list(background)]
    image=main_img
    image=cv2.imread("image.png")
    main_img[list(body)]=bg2[list(body)]
    img=cv2.addWeighted(main_img,0.7,image,0.3,0)
    return img
