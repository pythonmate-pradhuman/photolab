from cartoonize.white_box_cartoonizer.cartoonize import WB_Cartoonize
import cv2
from matplotlib import pyplot as plt


def toonify(img):
    wb_cartoonizer = WB_Cartoonize("cartoonize/white_box_cartoonizer/saved_models/", 0)
    img = wb_cartoonizer.infer(img)
    return img
