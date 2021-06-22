# import the necessary packages
from collections import OrderedDict

import numpy as np
import cv2
import argparse
import dlib
import imutils
from matplotlib import pyplot as plt
facial_features_cordinates = {}

# define a dictionary that maps the indexes of the facial
# landmarks to specific face regions
FACIAL_LANDMARKS_INDEXES = OrderedDict([
    ("Mouth", (48, 60)),
    ("Right_Eyebrow", (17, 21)),
    ("Left_Eyebrow", (22, 27)),
    ("Right_Eye", (36, 41)),
    ("Left_Eye", (42, 47)),
    ("Nose", (27, 35)),
    ("Jaw", (0, 17)),
    ("Lips", (61, 67))
])

# construct the argument parser and parse the arguments


def shape_to_numpy_array(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coordinates = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coordinates[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coordinates


def visualize_facial_landmarks(image, shape, colors=None, alpha=0.75):
    # create two copies of the input image -- one for the
    # overlay and one for the final output image
    overlay = image.copy()
    output = image.copy()

    # if the colors list is None, initialize it with a unique
    # color for each facial landmark region
    if colors is None:
        colors = [(19, 199, 109), (79, 76, 240), (230, 159, 23),
                  (168, 100, 168), (158, 163, 32),
                  (163, 38, 32), (180, 42, 220)]

    # loop over the facial landmark regions individually
    for (i, name) in enumerate(FACIAL_LANDMARKS_INDEXES.keys()):
        # grab the (x, y)-coordinates associated with the
        # face landmark
        (j, k) = FACIAL_LANDMARKS_INDEXES[name]
        pts = shape[j:k]
        facial_features_cordinates[name] = pts
        """
        # check if are supposed to draw the jawline
        if name == "Jaw":
            # since the jawline is a non-enclosed facial region,
            # just draw lines between the (x, y)-coordinates
            for l in range(1, len(pts)):
                ptA = tuple(pts[l - 1])
                ptB = tuple(pts[l])
                cv2.line(overlay, ptA, ptB, colors[i], 2)

        # otherwise, compute the convex hull of the facial
        # landmark coordinates points and display it
        else:
            hull = cv2.convexHull(pts)
            cv2.drawContours(overlay, [hull], -1, colors[i], -1)
        """
    # apply the transparent overlay
    #cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    # return the output image
    return facial_features_cordinates


def extract(org_image):
    image = org_image.copy()
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # load the input image, resize it, and convert it to grayscale
    #image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = shape_to_numpy_array(shape)

        output = visualize_facial_landmarks(image, shape)
        return output
        #plt.imshow(output)
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
def resizeAndPad(image, org_shape, padColor=0, sq_width=0, sq_height=0):
    img = image.copy()
    print("overlay_size", img.shape, org_shape)
    width_ratio = 1#img.shape[1]/image.shape[1]
    #568 is diff of center of eyes of specs
    ratios = (sq_width/568, sq_height/111)
    new_width = int(ratios[0]*img.shape[1])
    new_height = int(ratios[1]*img.shape[0])
    print("new_width: ", new_width, img.shape)
    #cv2.resize(img,(img.shape[1]//2,new_width),interpolation=cv2.INTER_CUBIC)
    #img = imutils.resize(img, width=new_width, inter="cubic")
    img = image_resize(img, width=new_width)
    print("new_width", new_width)
    c=cv2.imwrite("resover.png", img) 
    return (img, ratios)
    """
    ht, wd, cc= img.shape
    print("Shape", img.shape)
    print("org size", size)
    # create new image of desired size and color (blue) for padding
    hh, ww = size[:2]
    color = (0,0,0, 255)
    result = np.full((hh,ww,cc), color, dtype=np.uint8)

    # compute center offset
    xx = (ww - wd) // 2
    yy = (hh - ht) // 2
    
    # copy img image into center of result image
    result[yy:yy+ht, xx:xx+wd, :] = img
    return result
    """
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

    #overlay_image = overlay[..., :3] if background.shape[2] < 4 else overlay[..., :]
    overlay_image = overlay[..., :3]
    #overlay_image = overlay[0:(overlay.shape[0] if overlay.shape[0]>y+h else overlay.shape[0]-h), 0:(overlay.shape[1] if overlay.shape[1]>x+w else overlay.shape[1]-w),:3]
    mask = overlay[..., 3:] / 255.0
    
    #y2 = (back.shape[0] if back.shape[0]>(y+h) else y+h)
    
    #x2 = (back.shape[1] if back.shape[1]>(x+w) else x+w)
    

    print("***", background.shape, overlay_image.shape, y, y+h)
    print("***", background.shape, overlay_image.shape, x, x+w)
    print(mask.shape)
    #mask[mask>0]=1
    plt.imshow(mask)
    print("unique", np.unique(mask))
    if background.shape[2]<4:
        background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image
    else:
        background[y:y+h, x:x+w, :3] = (1.0 - mask) * background[y:y+h, x:x+w, :3] + mask * overlay_image
        m = mask*255
        print(m.shape)
        background[y:y+h, x:x+w, 3] = np.reshape(m, m.shape[0:2])
    #new_back = back.copy()
    return background

def putover(main_img, overlay):
    cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
    
    
def rotate_image(image, angle, point):
  image_center = point
  rot_mat = cv2.getRotationMatrix2D(image_center, -angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result