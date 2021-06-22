from rest_framework import viewsets
from . import serializers
from . import models
from file_app.models import File
from rest_framework import generics
import numpy as np
import cv2
import os
from PIL import Image
from rest_framework.response import Response
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from django.http import JsonResponse
from django.core.serializers import serialize


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
        img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        if action == 'FILTER':
            scale = 70
            width = int(img.shape[0] * scale / 100)
            height = int(img.shape[1] * scale / 100)
            img1 = cv2.resize(img, (width, height))
            img2 = cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path, os.pardir)), "pic25.png"))

            img2 = cv2.bitwise_not(img2)
            scale_fac = 50
            w = img1.shape[0]
            h = img1.shape[1]

            x = 0
            y = int(img1.shape[1] * scale_fac / 100)
            # crop image accor
            img3 = img1[x:w, y:h]
            img4 = cv2.resize(img2, img3.shape[1::-1])
            # img4 = cv2.resize(img2, (img3.shape[0], img3.shape[1]))
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
            img5 = cv2.imread(os.path.join(os.path.abspath(os.path.join(instance.file.path, os.pardir)), "back.jpg"))
            img5 = cv2.resize(img5, img1.shape[1::-1])
            gray1 = cv2.cvtColor(img5, cv2.COLOR_BGR2GRAY)

            res = cv2.addWeighted(sum1, 0.9, gray1, 1, 0)
            res = cv2.resize(res, img.shape[1::-1])
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
            res = img
        if action == 'editor':
            def GIF(img):
                # image = cv2.imread('hello1.jpg')
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower_red = np.array([99, 50, 30])
                upper_red = np.array([200, 255, 255])
                mask = cv2.inRange(hsv, lower_red, upper_red)
                mask3 = np.zeros_like(img)
                mask3[:, :, 0] = mask
                mask3[:, :, 1] = mask
                mask3[:, :, 2] = mask
                blue = cv2.bitwise_and(img, mask3)
                red = cv2.cvtColor(blue, cv2.COLOR_BGR2RGB)
                b, g, r = cv2.split(red)
                green = cv2.merge([g, r, b])
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                gray = cv2.bitwise_and(img, 255 - mask3)
                bluefinal = gray + blue
                redfinal = gray + red
                greenfinal = gray + green
                """
                cv2.imshow('blue', blue)
                cv2.imshow('gray', gray)
                cv2.imwrite("bluefinal.jpg", bluefinal)
                cv2.imshow("mask", mask)
                cv2.imshow("mask3", mask3)
                cv2.imshow("image", image)
                cv2.imshow("red",red)
                cv2.imwrite("redfinal.jpg",redfinal)
                cv2.imshow("green",green)
                cv2.imwrite("greenfinal.jpg",greenfinal)
                """
                import imageio
                images = [bluefinal, redfinal, greenfinal]  # here read all images
                imageio.mimsave("result1.gif", images, 'GIF', duration=0.2)
                """
                k = cv2.waitKey(0)
                if k == ord("s"):
                cv2.destroyAllWindows()
                """

        data = Image.fromarray(res)
        data.save("media/files/output" + str(instance.id) + ".png")
        # instance.processed_image.save('output.png', os.path.join( os.path.abspath( os.path.join( instance.file.path, os.pardir)),"output.png"))
        instance.processed_image = os.path.join(os.path.abspath(os.path.join(instance.file.path, os.pardir)),
                                                "output.png")
        processing_file = models.File.objects.get(id=instance.id)
        processing_file.processed_image = request.scheme + "://" + request.META[
            "HTTP_HOST"] + "/media/files/output" + str(instance.id) + ".png"
        processing_file.save()
        # with open(os.path.join(os.path.abspath(os.path.join(instance.file.path, os.pardir)), "output.png"), 'rb') as fi:
        # instance.processed_image = fi
        # instance.save()
        # print('instance.save()',instance.save())
        response = serialize('python', [processing_file], ensure_ascii=False)
        return JsonResponse(response, safe=False)
