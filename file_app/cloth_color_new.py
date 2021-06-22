# #import human_parsing2.human_parser as human_parser
# import numpy as np
# import PIL
# from PIL import Image, ImageDraw
# import cv2
# import cv2 as cv
# import imutils
# import human_parsing2.human_parser as human_parser
# import imageio
# import io
# import tensorflow as tf
# import os
# # Load compressed models from tensorflow_hub



# def resize_cartoon(img):
#     img3 = img.copy()
#     if img3.shape[0] > 540:
#         img3 = cv2.resize(img3, (0,0), fy=540/img3.shape[0], fx=540/img3.shape[0])
#     if img3.shape[1] > 540:
#         img3 = cv2.resize(img3, (0,0), fx=540/img3.shape[1], fy=540/img3.shape[1])
#     return img3
# def bifi(img):
#     temp = cv2.bilateralFilter(img, 9, 7, 9)
#     for i in range(8):
#         temp = cv2.bilateralFilter(temp, 9, 20, 0)
#     return temp

# def resize_shine2(img, dim):
#     row, col = dim
#     img_ratio = img.shape[0]/img.shape[1]
#     new_ratio = row/col
#     new_img = np.zeros((row, col, img.shape[2])).astype(np.uint8)
#     if img_ratio<new_ratio:
#         img = imutils.resize(img, height = row)
        
#         offset = int((img.shape[1] - col)/2)
#         new_img[:,:,:] = img[:, offset:col+offset,:]
#     if img_ratio>=new_ratio:
#         img = imutils.resize(img, width = col)
#         offset = int((img.shape[0] - row)/2)
#         new_img[:,:,:] = img[offset:row+offset,:,:]
#     return new_img

# def cloth_color_filter(main_img,back_img):
#     # back_img = cv2.imread("spray-wall.jpg")
#     main_img = resize_cartoon(main_img)
#     back_img = resize_shine2(back_img, (main_img.shape[0], main_img.shape[1]))

#     blue = main_img.copy()
#     blue[:,:,0] = np.minimum(255, blue[:,:,0]*5.5).astype(np.uint8)
#     blue[:,:,1] = np.minimum(255, blue[:,:,1]*1).astype(np.uint8)
#     blue[:,:,2] = np.minimum(255, blue[:,:,2]*1).astype(np.uint8)
#     blue = bifi(blue)

#     red = main_img.copy()
#     red[:,:,0] = np.minimum(255, red[:,:,0]*1).astype(np.uint8)
#     red[:,:,1] = np.minimum(255, red[:,:,1]*1).astype(np.uint8)
#     red[:,:,2] = np.minimum(255, red[:,:,2]*5.5).astype(np.uint8)
#     red = bifi(red)

#     sky = main_img.copy()
#     sky[:,:,0] = np.minimum(255, sky[:,:,0]*5.5).astype(np.uint8)
#     sky[:,:,1] = np.minimum(255, sky[:,:,1]*2.0).astype(np.uint8)
#     sky[:,:,2] = np.minimum(255, sky[:,:,2]*1).astype(np.uint8)
#     sky = bifi(sky)

#     parsed = human_parser.parse(main_img)

#     red[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))] = main_img[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))]
#     red[parsed==0] = back_img[parsed==0]

#     blue[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))] = main_img[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))]
#     blue[parsed==0] = back_img[parsed==0]

#     sky[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))] = main_img[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))]
#     sky[parsed==0] = back_img[parsed==0]

#     images = [blue, red, sky]# here read all images
#     fobj = io.BytesIO(b"")
#     imageio.mimsave(fobj, images, 'GIF', duration = 0.2)
#     binData = fobj.getvalue()

#     return binData


#import human_parsing2.human_parser as human_parser
import numpy as np
import PIL
from PIL import Image, ImageDraw
import cv2
import cv2 as cv
import imutils
import human_parsing2.human_parser as human_parser
import imageio
import io
import tensorflow as tf
import os
# Load compressed models from tensorflow_hub



def resize_cartoon(img):
    img3 = img.copy()
    if img3.shape[0] > 540:
        img3 = cv2.resize(img3, (0,0), fy=540/img3.shape[0], fx=540/img3.shape[0])
    if img3.shape[1] > 540:
        img3 = cv2.resize(img3, (0,0), fx=540/img3.shape[1], fy=540/img3.shape[1])
    return img3
def bifi(img):
    temp = cv2.bilateralFilter(img, 9, 7, 9)
    for i in range(8):
        temp = cv2.bilateralFilter(temp, 9, 20, 0)
    return temp

def resize_shine2(img, dim):
    row, col = dim
    img_ratio = img.shape[0]/img.shape[1]
    new_ratio = row/col
    new_img = np.zeros((row, col, img.shape[2])).astype(np.uint8)
    if img_ratio<new_ratio:
        img = imutils.resize(img, height = row)
        
        offset = int((img.shape[1] - col)/2)
        new_img[:,:,:] = img[:, offset:col+offset,:]
    if img_ratio>=new_ratio:
        img = imutils.resize(img, width = col)
        offset = int((img.shape[0] - row)/2)
        new_img[:,:,:] = img[offset:row+offset,:,:]
    return new_img

def cloth_color_filter(main_img,back_img):
    # back_img = cv2.imread("spray-wall.jpg")
    main_img = resize_cartoon(main_img)
    back_img = resize_shine2(back_img, (main_img.shape[0], main_img.shape[1]))

    blue = main_img.copy()
    blue[:,:,0] = np.minimum(255, blue[:,:,0]*5.5).astype(np.uint8)
    blue[:,:,1] = np.minimum(255, blue[:,:,1]*1).astype(np.uint8)
    blue[:,:,2] = np.minimum(255, blue[:,:,2]*1).astype(np.uint8)
    blue = bifi(blue)

    red = main_img.copy()
    red[:,:,0] = np.minimum(255, red[:,:,0]*1).astype(np.uint8)
    red[:,:,1] = np.minimum(255, red[:,:,1]*1).astype(np.uint8)
    red[:,:,2] = np.minimum(255, red[:,:,2]*5.5).astype(np.uint8)
    red = bifi(red)

    sky = main_img.copy()
    sky[:,:,0] = np.minimum(255, sky[:,:,0]*5.5).astype(np.uint8)
    sky[:,:,1] = np.minimum(255, sky[:,:,1]*2.0).astype(np.uint8)
    sky[:,:,2] = np.minimum(255, sky[:,:,2]*1).astype(np.uint8)
    sky = bifi(sky)

    #reducing size for faster computation
    img_small = imutils.resize(main_img, width=500, inter=cv2.INTER_CUBIC)

    parsed = human_parser.parse(img_small)
    # Making the mask bigger to match the original image size
    
    parsed = cv2.resize(parsed.astype(np.uint8), (main_img.shape[1], main_img.shape[0]))   
    

    red[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))] = main_img[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))]
    red[parsed==0] = back_img[parsed==0]

    blue[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))] = main_img[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))]
    blue[parsed==0] = back_img[parsed==0]

    sky[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))] = main_img[np.where(np.isin(parsed, [5,6,7,9,12], invert=True))]
    sky[parsed==0] = back_img[parsed==0]
    
    red = cv2.cvtColor(red, cv2.COLOR_BGR2RGB)
    blue = cv2.cvtColor(blue, cv2.COLOR_BGR2RGB)
    sky = cv2.cvtColor(sky, cv2.COLOR_BGR2RGB)
    
    images = [blue, red, sky]# here read all images
    fobj = io.BytesIO(b"")
    imageio.mimsave(fobj, images, 'GIF', duration = 0.2)
    binData = fobj.getvalue()

    return binData