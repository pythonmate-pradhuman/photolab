import numpy as np 
import cv2
import imutils
import human_parsing2.human_parser as human_parser

def resize_even(img, max_dim):
    new_img = img.copy()
    if new_img.shape[0] > max_dim:
        new_img = imutils.resize(new_img, height=max_dim)
    if new_img.shape[1] > max_dim:
        new_img = imutils.resize(new_img, width=max_dim)
    return new_img

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

def smoke_filter(img,smoke,smoke_frame):   
    img = resize_even(img, 1080)
    # smoke = cv2.imread("smoke.png")
    smoke = cv2.resize(smoke, (img.shape[1], img.shape[0]))
    # smoke_frame = cv2.imread("smoke-frame.png", -1)
    smoke_frame = cv2.resize(smoke_frame, (img.shape[1], img.shape[0]))

    # Making the image size small to get computation faster
    img_small = imutils.resize(img, width=500, inter=cv2.INTER_CUBIC)
   
    mask_big = human_parser.parse(img)

    # Making the mask bigger to match the original image size
    mask_big = cv2.resize(mask_big.astype(np.uint8), (img.shape[1], img.shape[0]))

    smoke[mask_big!=0] = img[mask_big!=0]
    final = overlay_transparent(smoke, smoke_frame, 0, 0)
    return final