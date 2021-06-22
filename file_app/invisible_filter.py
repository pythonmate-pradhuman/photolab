import human_parsing2.human_parser as human_parser
import numpy as np
import cv2


def invisible_filter(main_img,bg):
    body_parts = human_parser.parse(main_img)
    clothes=np.array(np.where(np.isin(body_parts,[1,3,4,5,6,7,8,9,11,12,18,19])))
    background=np.array(np.where(body_parts==0)) 
    # bg=cv2.imread("background.jpg")
    bg=cv2.resize(bg,(main_img.shape[1],main_img.shape[0]))
    main_img[list(background)]=bg[list(background)]
    img=cv2.addWeighted(main_img, 0.6, bg, 0.4, 0)
    img[list(clothes)]=main_img[list(clothes)]
    return img