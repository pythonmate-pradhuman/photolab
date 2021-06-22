import numpy as np 
import cv2
from matplotlib import pyplot as plt
import imutils
from PIL import Image, ImageEnhance
import human_parsing2.human_parser as human_parser

def resize_even(img, max_dim):
    new_img = img.copy()
    if new_img.shape[0] > max_dim:
        new_img = imutils.resize(new_img, height=max_dim)
    if new_img.shape[1] > max_dim:
        new_img = imutils.resize(new_img, width=max_dim)
    return new_img

    
def enhance(img, brightness):
    mask = img[:,:,3:4]
    img2 = img.copy()
    img2 = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    sharp = ImageEnhance.Contrast(img2)
    img2 = sharp.enhance(brightness)
    img2 = np.array(img2)
    
    img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
    
    return np.concatenate((img2,mask), axis=2)

def overlay_transparent(back, over, x, y):

    background = back.copy()
    overlay=over.copy()
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
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
   
    mask = overlay[..., 3:] / 255.0
  
    if background.shape[2]<4:
        background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image
    else:
        background[y:y+h, x:x+w, :3] = (1.0 - mask) * background[y:y+h, x:x+w, :3] + mask * overlay_image
        m = mask*255
        background[y:y+h, x:x+w, 3] = np.reshape(m, m.shape[0:2])
    
    return background

def shake(img, kernal):
    main_img = img.copy()
    kernel_size = kernal

    # Create the vertical kernel. 
    kernel_v = np.zeros((kernel_size, kernel_size)) 

    # Create a copy of the same for creating the horizontal kernel. 
    kernel_h = np.copy(kernel_v) 

    # Fill the middle row with ones. 
    kernel_v[:, int((kernel_size - 1)/2)] = np.ones(kernel_size) 
    kernel_h[int((kernel_size - 1)/2), :] = np.ones(kernel_size) 

    # Normalize. 
    kernel_v /= kernel_size 
    kernel_h /= kernel_size 

    # Apply the vertical kernel. 
    #vertical_mb = cv2.filter2D(img, -1, kernel_v) 

    # Apply the horizontal kernel. 
    horizonal_mb = cv2.filter2D(main_img, -1, kernel_h) 
    return horizonal_mb


def shake_filter(img,img_back):
    # img_back = cv2.imread("./sprit-back.jpg")
    img = resize_even(img, 1080)
    img_back = cv2.resize(img_back, (img.shape[1], img.shape[0]))

    # Making the image size small to get computation faster
    img_small = imutils.resize(img, width=500, inter=cv2.INTER_CUBIC)

    # Using the sengmentation parser on smaller image to get mask
    mask = human_parser.parse(img_small)

    # Making the mask bigger to match the original image size
    mask_big = cv2.resize(mask.astype(np.uint8), (img.shape[1], img.shape[0]))#imutils.resize(mask.astype(float), height=img.shape[0], width=img.shape[1], inter=cv2.INTER_CUBIC)


    img2 = img.copy()
    img2 = enhance(img2, 0.8)
    img2[:,:,0] = np.minimum(255, img2[:,:,0]*1.8)
    img2[:,:,1] = np.minimum(255, img2[:,:,1]*1.2)
    img2[:,:,2] = img2[:,:,2]*0.4
    img2[mask_big==0] = img_back[mask_big==0]
    img2 = shake(img2, 5)
    #img2 = enhance(img2, 1)


    img3 = img.copy()
    #img3 = enhance(img3, 0.5)
    img3[:,:,0] = np.minimum(255, img3[:,:,0]*0.4)
    img3[:,:,1] = np.minimum(255, img3[:,:,1]*1.8)
    img3[:,:,2] = np.minimum(255, img3[:,:,2]*1.8)
    img3[mask_big==0] = [255, 255, 255]
    img3 = shake(img3, 80)

    #img3 = enhance(img3, 1)

    fore=np.where(mask_big!=0)
    topLeft=(np.min(fore[0]), np.min(fore[1]))
    rightBottom=(np.max(fore[0]), np.max(fore[1]))

    trans = mask_big.copy()



    for i in range(topLeft[0], rightBottom[0]):
        row = trans[i,:]
        color_strip = np.where(row>0)
        mx = np.max(color_strip)
        mn = np.min(color_strip)
        strip_width= mx - mn
        for j in range(mn, mx+1):
            row[j] = int(255*(1- ((i-topLeft[0])/(rightBottom[0]-topLeft[0]))))*0.1  + int(255*((j-mn)/strip_width)**2)*0.9

    trans.shape = (trans.shape[0],trans.shape[1], 1)
    img4 = np.concatenate((img3, trans), axis=2)
    a=np.zeros(img2.shape).astype(np.uint8)
    shift = int(img4.shape[1]*0.13)
    final = overlay_transparent(img2, img4[:,:-shift,:], shift, 0)
    return final