import cv2
import numpy as np
import human_parsing2.human_parser as human_parser
import cartoonize.toonify as toonify
import math
import imutils

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


def cartoon_tear(img, back_img, inner_img):
    # back_img = cv2.imread("cartoon-snake.png", -1)

    img2 = resize_cartoon(img)
    # Making the image size small to get computation faster
    img_small = imutils.resize(img2, width=500, inter=cv2.INTER_CUBIC)

    # Using the sengmentation parser on smaller image to get mask
    mask = human_parser.parse(img_small)

    # Making the mask bigger to match the original image size
    parsed = cv2.resize(mask.astype(np.uint8), (img2.shape[1], img2.shape[0]))

    img2 = toonify.toonify(img2.astype(int))

    img2 = cv2.resize(img2, (parsed.shape[1], parsed.shape[0]))
    back_img = cv2.resize(back_img, (parsed.shape[1], parsed.shape[0]))
    inner_img = cv2.resize(inner_img, (parsed.shape[1], parsed.shape[0]))

    colored = np.where(parsed != 0)
    xmin = np.min(colored[1])
    xmax = np.max(colored[1])
    human_width = xmax-xmin
    human = img2[:, xmin:xmax, :]
    parsed = parsed[:, xmin:xmax]

    human2 = cv2.resize(human, (int(
        0.8*back_img.shape[1]), int((0.8*back_img.shape[1]/human.shape[1])*human.shape[0])))
    human2 = cv2.resize(human2, (int(
        (0.8*back_img.shape[0]/human.shape[0])*human.shape[1]), int(0.8*back_img.shape[0])))
    parsed2 = cv2.resize(parsed.astype(np.uint8),
                         (human2.shape[1], human2.shape[0]))

    back_img2 = back_img.copy()
    back_img2 = back_img2[:, :, :3]

    # back_img2[back_img[:, :, 3] < 250] = [18, 109, 242]
    back_img2[back_img[:, :, 3] < 250] = inner_img[:,
                                                   :, :3][back_img[:, :, 3] < 250]

    padx = int((back_img2.shape[1]-human2.shape[1])/2)
    pady = int((back_img2.shape[0]-human2.shape[0])/2)
    cut = back_img2[pady:pady+human2.shape[0], padx:padx+human2.shape[1], :]
    cut[parsed2 != 0] = human2[parsed2 != 0]
    back_img2[pady:pady+human2.shape[0], padx:padx+human2.shape[1], :] = cut

    back_img3 = back_img.copy()

    top = int(back_img3.shape[0] * 0.5)
    for i in range(top, pady+human2.shape[0]):
        for j in range(padx, padx+human2.shape[1]):
            if back_img3[i, j, 3] < 250 and parsed2[i-pady, j-padx] != 0:
                back_img3[i, j, :3] = human2[i-pady, j-padx, :]
            elif back_img3[i, j, 3] < 250:
                # back_img3[i, j, :3] = [18, 109, 242]
                back_img3[i, j, :3] = inner_img[i, j, :3]
            back_img3[i, j, 3] = 255
    # back_img3[back_img3[:, :, 3] < 250] = [18, 109, 242, 255]
    back_img3[back_img3[:, :, 3] < 250] = inner_img[back_img3[:, :, 3] < 250]

    back_img2[top:, :, :3] = back_img3[top:, :, :3]
    return back_img2
