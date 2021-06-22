
from .face_features import *
import human_parsing2.human_parser as human_parser
from matplotlib import pyplot as plt
import cv2
import math




def apply(main_img):

    main_img = cv2.cvtColor(main_img, cv2.COLOR_BGR2RGB)
    overlay = cv2.imread("overlay8.png", cv2.IMREAD_UNCHANGED)
    left_overlay = cv2.imread("left_overlay2.png", cv2.IMREAD_UNCHANGED)
    right_overlay = cv2.imread("right_overlay2.png", cv2.IMREAD_UNCHANGED)
    stars = cv2.imread("stars.png", cv2.IMREAD_UNCHANGED)

    if main_img.shape[0]>1080:
        main_img = imutils.resize(main_img, height=1080)
    if main_img.shape[1]>1080:
        main_img = imutils.resize(main_img, width=1080)
        
    
    left_overlay = cv2.resize(left_overlay, (int((main_img.shape[0]/left_overlay.shape[0])*left_overlay.shape[1]), main_img.shape[0]), interpolation = cv2.INTER_AREA) 
    right_overlay = cv2.resize(right_overlay, (int((main_img.shape[0]/right_overlay.shape[0])*right_overlay.shape[1]), main_img.shape[0]), interpolation = cv2.INTER_AREA) 
    left_overlay = left_overlay[:,:main_img.shape[1],:]
    right_overlay = right_overlay[:,-main_img.shape[1]:,:]
    if right_overlay.shape[1]<main_img.shape[1]:
        right_overlay = np.concatenate((np.zeros((main_img.shape[0], main_img.shape[1]-right_overlay.shape[1], 4)), right_overlay), axis=1)
    ratio = main_img.shape[1]/stars.shape[1] if main_img.shape[1]<stars.shape[1] else 1

    ratio = main_img.shape[0]/stars.shape[0] if main_img.shape[0]<stars.shape[0] else 1

    stars = cv2.resize(stars, (int(stars.shape[1]*ratio), int(stars.shape[0]*ratio)), interpolation = cv2.INTER_AREA) 

    features = extract(main_img)

    left_mean = np.mean(features["Right_Eye"], axis=0)
    right_mean = np.mean(features["Left_Eye"], axis=0)
    eyes = np.concatenate((features["Right_Eye"], features["Left_Eye"]))

    l = left_mean[0]
    r = right_mean[0]

    u = (left_mean[1]+right_mean[1])/2
    mid = (r+l)/2
    a_w = r-l

    pos_x = l
    pos_y = u

    angle = math.degrees(math.atan((left_mean[1]-right_mean[1])/(l-r)))

    # Making the image size small to get computation faster
    img_small = imutils.resize(main_img, width=500, inter=cv2.INTER_CUBIC)

    # Using the sengmentation parser on smaller image to get mask
    mask = human_parser.parse(img_small)

    # Making the mask bigger to match the original image size
    body_parts = cv2.resize(mask.astype(np.uint8), (main_img.shape[1], main_img.shape[0]))#imutils.resize(mask.astype(float), height=img.shape[0], width=img.shape[1], inter=cv2.INTER_CUBIC)
    
    no_clothes = np.array(np.where(np.isin(body_parts,[3,5,6,7,8,9,10,11,12])==False))
    no_background = np.array(np.where(body_parts != [0]))


    (over, ratios) = resizeAndPad(overlay, org_shape=main_img.shape, padColor=0, sq_width=a_w, sq_height=0)

    pos_x = int(pos_x-628*ratios[0])
    pos_y = int(pos_y-1240*ratios[0])

    if pos_x<0:
        over = over[:, -pos_x: ,:]
        pos_x=0
    if pos_y<0:
        over = over[-pos_y: ,:,:]
        pos_y=0

    overlay_layer = np.zeros((main_img.shape[0], main_img.shape[1], main_img.shape[2]+1))

    overlay_layer = overlay_transparent(overlay_layer, over, pos_x, pos_y)

    overlay_layer = rotate_image(overlay_layer, angle, ((r+l)/2, u))


    np.min(overlay_layer)



    def filter_sides(side, no_back):
        no_backnew = [[],[]]
        for i in range(len(no_back[0])):
            if no_back[0][i] < side.shape[0] and no_back[1][i] < side.shape[1]:
                no_backnew[0].append(no_back[0][i])
                no_backnew[1].append(no_back[1][i])
        return no_backnew
    stars_back = filter_sides(stars, no_clothes)
    stars[stars_back[0], stars_back[1],:]=0

    left_back = filter_sides(left_overlay, no_background)
    right_back = filter_sides(right_overlay, no_background)
    left_overlay[left_back[0], left_back[1], :]=0
    right_overlay[right_back[0], right_back[1], :]=0


    final = overlay_transparent(final, left_overlay, 0, 0)
    final = overlay_transparent(final, right_overlay, 0, 0)

    return (final)

        