import cv2
from PIL import Image
from human_parsing2 import  human_parser
import numpy as np
def remove_background(img):

    # getting body parts
    body_parts = human_parser.parse(img)

    # getting background
    background=np.array(np.where(body_parts==0))

    #convertng from 2d to 3d
    bg=np.stack((body_parts,)*3, axis=-1)

    # replacing backgroung of image to black
    img[list(background)]=bg[list(background)]

    # conveting to pillow
    pilimg=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # converting to rgba
    pilimg = pilimg.convert("RGBA")
    
    # conveting background to transparent
    datas = pilimg.getdata()

    newData = []

    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    # converting to cv2 
    open_cv_image = np.array(pilimg) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    return open_cv_image