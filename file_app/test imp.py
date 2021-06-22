from rest_framework import viewsets
from . import serializers
from . import models
from file_app.models import File
from rest_framework import generics
import numpy as np
import cv2
import os
from PIL import Image
import imutils
import math
import imageio
import io
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import redirect,HttpResponse,HttpResponseRedirect

def overlay_transparent(back, over, x, y):
    background = back.copy()
    overlay = over.copy()
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
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype) * 255
            ],
            axis=2,
        )

    # overlay_image = overlay[..., :3] if background.shape[2] < 4 else overlay[..., :]
    overlay_image = overlay[..., :3]
    # overlay_image = overlay[0:(overlay.shape[0] if overlay.shape[0]>y+h else overlay.shape[0]-h), 0:(overlay.shape[1] if overlay.shape[1]>x+w
    mask = overlay[..., 3:] / 255.0

    # y2 = (back.shape[0] if back.shape[0]>(y+h) else y+h)

    # x2 = (back.shape[1] if back.shape[1]>(x+w) else x+w)

    if background.shape[2] < 4:
        background[y:y + h, x:x + w] = (1.0 - mask) * background[y:y + h, x:x + w] + mask * overlay_image
    else:
        background[y:y + h, x:x + w, :3] = (1.0 - mask) * background[y:y + h, x:x + w, :3] + mask * overlay_image
        m = mask * 255
        print(m.shape)
        background[y:y + h, x:x + w, 3] = np.reshape(m, m.shape[0:2])
    # new_back = back.copy()
    return background


def rotate_image(img, angle):
    dig_len = int(math.sqrt(img.shape[0] ** 2 + img.shape[1] ** 2))
    print("dig_len", dig_len)
    new_img = np.zeros((dig_len, dig_len, 4), np.uint8)
    diff_x = dig_len - img.shape[1];
    diff_y = dig_len - img.shape[0];
    print("dif_x", diff_x)
    new_img[int(diff_y / 2):img.shape[0] + int(diff_y / 2), int(diff_x / 2):img.shape[1] + int(diff_x / 2), :] = img
    img = new_img
    height, width = (img.shape[0], img.shape[1])
    size = (width, height)
    center = (width / 2, height / 2)
    dst_mat = np.zeros((height, width, 4), np.uint8)
    scale = 1
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    img_dst = cv2.warpAffine(img, rotation_matrix, size, dst_mat, flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_TRANSPARENT)
    return img_dst


#########################################################MAIN CODE###################################################################

def filter(image,instance):
    print('filterfunction',image.shape)
    background0 = cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path,os.pardir)),"white.jpg"))
    fourth_ch = np.zeros(background0.shape[0:2])
    fourth_ch[:, :] = 255
    fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
    background = background0
    print("#######################################################################")
    if (image.shape[0] < image.shape[1]):
        backhori = cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path,os.pardir)),"back_hori.png"),-1)
        cv2.imwrite('test.jpg',backhori)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if image.shape[0] > 330 or image.shape[0] < 330:
            image = imutils.resize(image, height=330)
        presketch = imutils.resize(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), height=470)
        fourth_ch = np.zeros(image.shape[0:2])
        fourth_ch[:, :] = 255
        fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
        image = np.concatenate((image, fourth_ch), axis=2)
        sketch = np.stack((presketch,) * 3, axis=-1)
        fourth_ch = np.zeros(sketch.shape[0:2])
        fourth_ch[:, :] = 255
        fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
        sketch = np.concatenate((sketch, fourth_ch), axis=2)
        image = rotate_image(image, 14)
        sketch = rotate_image(sketch, 347)
        background = overlay_transparent(background, sketch, 250, 70)
        background = overlay_transparent(background, image, 10, 400)
        final = overlay_transparent(background, backhori, 0, 0)


    elif (image.shape[0] > image.shape[1]):
        backverti = cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path,os.pardir)),"back_verti.png"),-1)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if image.shape[1] > 345 or image.shape[1] < 345:
            image = imutils.resize(image, width=345)
        presketch = imutils.resize(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), width=520)
        cv2.imwrite('test.jpg',presketch)
        fourth_ch = np.zeros(image.shape[0:2])
        fourth_ch[:, :] = 255
        fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
        image = np.concatenate((image, fourth_ch), axis=2)
        sketch = np.stack((presketch,) * 3, axis=-1)
        fourth_ch = np.zeros(sketch.shape[0:2])
        fourth_ch[:, :] = 255
        fourth_ch.shape = (fourth_ch.shape[0], fourth_ch.shape[1], 1)
        sketch = np.concatenate((sketch, fourth_ch), axis=2)
        image = rotate_image(image, 14)
        sketch = rotate_image(sketch, 348)
        background = overlay_transparent(background, sketch, 170, 80)
        background = overlay_transparent(background, image, 0, 395)
        final = overlay_transparent(background, backverti, 0, 0)
    return (final)


#########EXAMPLE#########

# image = cv2.imread('hello.jpg')
# fina = filter(image,instance)
# cv2.imwrite("final.jpg", fina)


def shine_filter(main_img,instance):
    kelvin_table = {
        1000: (255, 56, 0),
        1500: (255, 109, 0),
        2000: (255, 137, 18),
        2500: (255, 161, 72),
        3000: (255, 180, 107),
        3500: (255, 196, 137),
        4000: (255, 209, 163),
        4500: (255, 219, 186),
        5000: (255, 228, 206),
        5500: (255, 236, 224),
        6000: (255, 243, 239),
        6500: (255, 249, 253),
        7000: (245, 243, 255),
        7500: (235, 238, 255),
        8000: (227, 233, 255),
        8500: (220, 229, 255),
        9000: (214, 225, 255),
        9500: (208, 222, 255),
        10000: (204, 219, 255)}

    def convert_temp(main_img, temp):
        # You may need to convert the color.
        main_img = cv2.cvtColor(main_img.copy(), cv2.COLOR_BGR2RGB)
        main_img = Image.fromarray(main_img)
        r, g, b = kelvin_table[temp]
        matrix = (r / 255.0, 0.0, 0.0, 0.0,
                  0.0, g / 255.0, 0.0, 0.0,
                  0.0, 0.0, b / 255.0, 0.0)
        return cv2.cvtColor(np.asarray(main_img.convert('RGB', matrix)), cv2.COLOR_RGB2BGR)

    background =cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path,os.pardir)),"face_shine_back.png"))

    main_img = convert_temp(main_img, 10000)

    def apply_brightness_contrast(input_img, brightness=0, contrast=0):

        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow) / 255
            gamma_b = shadow

            buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
        else:
            buf = input_img.copy()

        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127 * (1 - f)

            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

        return buf
    main_img = apply_brightness_contrast(main_img.copy(), brightness=-60, contrast=38)
    main_img = cv2.resize(main_img, (540, 540))
    main_img = cv2.addWeighted(main_img, 1, background, 1, 0)
    return main_img


class ImageViewset(viewsets.ModelViewSet):  #
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = serializers.FileSerializer(instance)
        file = instance.file.path
        action = request.data['action']
        src = cv2.imread(instance.file.path)
        img = src
        # img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        if action == 'FILTER':
            scale = 70
            width = int(img.shape[0] * scale / 100)
            height = int(img.shape[1] * scale / 100)
            img1 = cv2.resize(img, (width, height))
            img2 = cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path,os.pardir)), "pic25.png"))

            img2 = cv2.bitwise_not(img2)
            scale_fac = 50
            w = img1.shape[0]
            h = img1.shape[1]

            x = 0
            y = int(img1.shape[1] * scale_fac / 100)
            # crop image accor
            img3 = img1[x:w, y:h]
            img4=cv2.resize(img2, img3.shape[1::-1])
            #img4 = cv2.resize(img2, (img3.shape[0], img3.shape[1]))
            dst1 = cv2.bitwise_or(img3, img4)

            dst1[np.where((dst1 == [255, 255, 255]).all(axis=2))] = [211, 211, 211]

            # to place a pic at y
            rows, cols, channels = dst1.shape

            roi1 = dst1[0:rows, 0:cols]
            img1[0:w, y:y + cols] = roi1
            gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

            (thresh, blawh) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            blur = cv2.GaussianBlur(blawh, (37, 37), 0)
            sum1 = cv2.addWeighted(blur, 0.3, gray, 0.9, 0)

            # providing effect
            img5 = cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path,os.pardir)), "back.jpg"))
            img5 = cv2.resize(img5, img1.shape[1::-1])
            gray1 = cv2.cvtColor(img5, cv2.COLOR_BGR2GRAY)

            img = cv2.addWeighted(sum1, 0.9, gray1, 1, 0)
            img = cv2.resize(img, img.shape[1::-1])
        if action == 'FILTER_MOTIVATION':
            # img=cv2.imread("moti4.jpg",-1)
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            img4 = cv2.imread(
                (os.path.join(os.path.abspath(os.path.join(instance.file.path, os.pardir)), "motivational.png")),
                cv2.IMREAD_UNCHANGED)

            dim = (img.shape[1], img.shape[0])
            # resize image
            img4 = cv2.resize(img4, dim, interpolation=cv2.INTER_AREA)
            # added_image = cv2.addWeighted(img3,0.4,img,0.1,0)
            gw, gh, gc = img4.shape
            x = 0
            y = 0
            for i in range(0, gw):
                for j in range(0, gh):
                    if img4[i, j][3] != 0:
                        img[y + i, x + j] = img4[i, j]

            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        if action == 'GIF':
            image = img
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower_red = np.array([99, 50, 30])
            upper_red = np.array([200, 255, 255])
            mask = cv2.inRange(hsv, lower_red, upper_red)
            mask3 = np.zeros_like(image)
            mask3[:, :, 0] = mask
            mask3[:, :, 1] = mask
            mask3[:, :, 2] = mask
            blue = cv2.bitwise_and(image, mask3)
            red = cv2.cvtColor(blue, cv2.COLOR_BGR2RGB)
            b, g, r = cv2.split(red)
            green = cv2.merge([g, r, b])
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            gray = cv2.bitwise_and(img, 255 - mask3)
            bluefinal = gray + blue
            redfinal = gray + red
            greenfinal = gray + green

            img = [bluefinal, redfinal, greenfinal]  # here read all images
            obj = io.BytesIO(b"")
            imageio.mimsave(obj, img, 'GIF', duration=0.2)
            # Example use ----------------------
            f2 = open('./media/files/output'+ str(instance.id) +'.gif', "wb+")
            processed_image = request.scheme + "://" + request.META["HTTP_HOST"] + "/media/files/output" + str(instance.id) + ".gif"
            f2.write(obj.getvalue())


        if action == 'SHINEFILTER':
            img = shine_filter(img,instance)
            print('imgshine',img)

            # status = cv2.imwrite('./media/files/output' + str(instance.id) + '.jpg', img)
            # processed_file = request.scheme + "://" + request.META["HTTP_HOST"] + "/media/files/output" + str(instance.id) + ".jpg"
            # print("Image written to file-system : ", status)


        if action =='ROTATE':
            img = filter(img, instance)
            print('imgshine', img)
            # status = cv2.imwrite('./media/files/output' + str(instance.id) + '.jpg', img)
            # processed_file = request.scheme + "://" + request.META["HTTP_HOST"] + "/media/files/output" + str(instance.id) + ".jpg"
            # print("Image written to file-system : ", status)

        if action == "GIF":
            pass
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res=img


        if action=='GIF':
            pass
        else:
            data = Image.fromarray(res)
            data.save("media/files/output" + str(instance.id) + ".png")
            processed_image = request.scheme + "://" + request.META["HTTP_HOST"] + "/media/files/output" + str(instance.id) + ".png"
        # instance.processed_image.save('output.png', os.path.join( os.path.abspath( os.path.join( instance.file.path, os.pardir)),"output.png"))
        if action == "GIF":
            instance.processed_image = os.path.join(os.path.abspath(os.path.join(instance.file.path, os.pardir)),"output.gif")
        else:
            instance.processed_image = os.path.join(os.path.abspath(os.path.join(instance.file.path, os.pardir)),"output.png")
        processing_file = models.File.objects.get(id=instance.id)
        processing_file.processed_image = processed_image
        processing_file.save()
        # with open(os.path.join(os.path.abspath(os.path.join(instance.file.path, os.pardir)), "output.png"), 'rb') as fi:
        # instance.processed_image = fi
        # instance.save()
        # print('instance.save()',instance.save())
        response = serialize('python', [processing_file], ensure_ascii=False)
        return JsonResponse(response, safe=False)






