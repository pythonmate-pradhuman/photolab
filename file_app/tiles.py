
from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
from PIL import Image, ImageEnhance

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



def redify(img):
    img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    r, g, b = (255,80,80)
    matrix = ( r / 255.0, 0.0, 0.0, 0.0,
               0.0, g / 255.0, 0.0, 0.0,
               0.0, 0.0, b / 255.0, 0.0 )
    return cv2.cvtColor(np.asarray(img.convert('RGB', matrix)), cv2.COLOR_RGB2BGR)


def enhance(img, brightness):
    mask = img[:,:,3:4]
    img2 = img.copy()
    
    img2 = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    bright = ImageEnhance.Brightness(img2)
    img2 = bright.enhance(brightness)
    sharp = ImageEnhance.Sharpness(img2)
    img2 = sharp.enhance(3)
    contrast = ImageEnhance.Contrast(img2)
    img2 = contrast.enhance(2.2)
    img2 = np.array(img2)
    
    img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
    img2 = redify(img2)
    return np.concatenate((img2,mask), axis=2)

def apply_tile(img, tile, brightness):
    img2 = img.copy()
    
    mask = tile[:,:,3]
    black_pos = np.where(mask[:,:]<200)
    img2[black_pos]=[0,0,0]
    mask.shape = (mask.shape[0], mask.shape[1],1)
    img2 = np.concatenate((img2,mask), axis=2)
    img2 = img2[:,50:-50,:]
    img2 = enhance(img2, brightness)
    return img2
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

def tiles_filter(img,tile1,tile2,tile3,tile4,tile5):
    # tile1 = cv2.imread("tiles/tile1.png", -1)
    # tile2 = cv2.imread("tiles/tile2.png", -1)
    # tile3 = cv2.imread("tiles/tile3.png", -1)
    # tile4 = cv2.imread("tiles/tile4.png", -1)
    # tile5 = cv2.imread("tiles/tile5.png", -1)
    if (img.shape[1]/img.shape[0]) <0.8:
        img = resize_shine2(img, tile5.shape[0:2])
        fin1 = apply_tile(img, tile1, 0.6)
        fin2 = apply_tile(img, tile2, 0.6)
        fin3 = apply_tile(img, tile3, 0.6)
        fin4 = apply_tile(img, tile4, 0.6)
        fin5 = apply_tile(img, tile5, 0.6)
        final = np.zeros((img.shape[0], img.shape[1], 3)).astype(np.uint8)
        final[:,:,:] = [133, 188, 255]

        final = overlay_transparent(final, fin5, 80, 0)
        final = overlay_transparent(final, fin4, 0, 0)
        final = overlay_transparent(final, fin3, 50, 0)
        final = overlay_transparent(final, fin2, 20, 0)
        final = overlay_transparent(final, fin1, 90, 0)
    else:
        tile1 = tile1[0:-200,:,:]
        tile2 = tile2[0:-200,:,:]
        tile3 = tile3[0:-200,:,:]
        tile4 = tile4[0:-200,:,:]
        img = resize_shine2(img, tile4.shape[0:2])
        fin1 = apply_tile(img, tile1, 0.6)
        fin2 = apply_tile(img, tile2, 0.6)
        fin3 = apply_tile(img, tile3, 0.6)
        fin4 = apply_tile(img, tile4, 0.6)
        final = np.zeros((img.shape[0], img.shape[1], 3)).astype(np.uint8)
        final[:,:,:] = [133, 188, 255]

        final = overlay_transparent(final, fin4, 0, 0)
        final = overlay_transparent(final, fin3, 50, 0)
        final = overlay_transparent(final, fin2, 20, 0)
        final = overlay_transparent(final, fin1, 90, 0)
    
    
    return final
    