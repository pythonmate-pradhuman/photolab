import io
import json
import math
import os

import cartoonize.toonify as toonify
import cv2
import cv2 as cv
import imageio
import imutils
import numpy as np
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect
from rest_framework.response import Response
from matplotlib import pyplot as plt
from PIL import Image
from rest_framework import generics, viewsets
from rest_framework.views import APIView

from file_app.models import File
from CustomFilters.models import CustomFilters

from . import models, serializers
from .cartoon_filter import cartoon_filter
from .filter_motivation import filter_motivation
from .gif_filter import gif_filter
from .normal_filter import normal_filter
from .rotate_filter import filter
from .shine_filter import shine_filter
from .news_paper import apply
from .red_blue import red_blue
from .shaking import shake_filter
from .tiles import tiles_filter
from .cloth_color import cloth_color_filter
from .smoke import smoke_filter
from .cartoon_tear import cartoon_tear
from .triple_exposer import triple_exposer
from .invisible_filter import invisible_filter
from .duck_gif import duck_gif
from .duck_gif import custom_duck_gif
import json
from rest_framework.pagination import PageNumberPagination


class ImageViewset(viewsets.ModelViewSet):  #
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            print("trying...")
            __custom_filter = int(request.data.get("custom_filter"))
        except:
            print("exception handled....")
            __custom_filter = None
        if __custom_filter is not None:
            custom = CustomFilters.objects.get(id=__custom_filter)
            data = request.data
            data._mutable = True
            data.update({"action": custom.action})
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)
            instance_serializer = serializers.FileSerializer(instance)
            file = instance.file.path

            action = custom.action
            print("file path....", instance.file.path)
            src = cv2.imread(file)
            img = src
            # img=crop_image(img)
            print(img)
            if action == 'FILTER':
                print("name", custom.bg_image_1.name)

                img2 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_1.path, os.pardir)), custom.bg_image_1.name.split("/")[-1]))
                img5 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_2.path, os.pardir)), custom.bg_image_2.name.split("/")[-1]))
                # img2 = custom.bg_image_1
                # img5 = custom.bg_image_2
                print("img2", img2, "img5", img5)
                img = normal_filter(img, img2, img5)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'CARTOON_TEAR':
                # back_img = cv2.imread(os.path.join(os.path.abspath(os.path.join(
                #     instance.file.path, os.pardir)), "cartoon-snake.png"), -1)
                back_img = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_1.path, os.pardir)), custom.bg_image_1.name.split("/")[-1]), -1)
                inner_img = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_1.path, os.pardir)), custom.bg_image_1.name.split("/")[-1]), -1)
                img = cartoon_tear(img, back_img, inner_img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'SHAKING':
                # img_back = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "sprit-back.jpg"))
                img_back = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_1.path, os.pardir)), custom.bg_image_1.name.split("/")[-1]))
                img = shake_filter(img, img_back)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'TILES':
                # tile1 = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "tile1.png"), -1)
                # tile2 = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "tile2.png"), -1)
                # tile3 = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "tile3.png"), -1)
                # tile4 = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "tile4.png"), -1)
                # tile5 = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "tile5.png"), -1)
                tile1 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_1.path, os.pardir)), custom.bg_image_1.name.split("/")[-1]), -1)
                tile2 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_2.path, os.pardir)), custom.bg_image_2.name.split("/")[-1]), -1)
                tile3 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_3.path, os.pardir)), custom.bg_image_3.name.split("/")[-1]), -1)
                tile4 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_4.path, os.pardir)), custom.bg_image_4.name.split("/")[-1]), -1)
                tile5 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_5.path, os.pardir)), custom.bg_image_5.name.split("/")[-1]), -1)
                img = tiles_filter(img, tile1, tile2, tile3, tile4, tile5)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'CLOTH_COLOR_FILTER':
                # back_img = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "spray-wall.jpg"))
                back_img = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_1.path, os.pardir)), custom.bg_image_1.name.split("/")[-1]))
                obj = cloth_color_filter(img, back_img)
                f2 = open('./media/output/images/output' +
                          str(instance.id) + '.gif', "wb+")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".gif"
                f2.write(obj)

            if action == 'SMOKE_FILTER':
                # smoke = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "smoke.png"))
                # smoke_frame = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "smoke-frame.png"), -1)
                smoke = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_1.path, os.pardir)), custom.bg_image_1.name.split("/")[-1]))
                smoke_frame = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_2.path, os.pardir)), custom.bg_image_2.name.split("/")[-1]), -1)
                img = smoke_filter(img, smoke, smoke_frame)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'FILTER_MOTIVATION':
                # img4 = cv2.imread(
                #     (os.path.join(os.path.abspath(os.path.join(
                #         instance.file.path, os.pardir)), "motivational.png")),
                #     cv2.IMREAD_UNCHANGED)
                img4 = cv2.imread(
                    (os.path.join(os.path.abspath(os.path.join(
                        custom.bg_image_1.path, os.pardir)), custom.bg_image_1.name.split("/")[-1])),
                    cv2.IMREAD_UNCHANGED)
                img = filter_motivation(img, img4)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'NEWS_PAPER':
                # news = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "news.jpeg"))
                # words = cv2.imread(os.path.join(os.path.abspath(
                #     os.path.join(instance.file.path, os.pardir)), "words.jpeg"))
                news = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_1.path, os.pardir)), custom.bg_image_1.name.split("/")[-1]))
                words = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(custom.bg_image_2.path, os.pardir)), custom.bg_image_2.name.split("/")[-1]))
                img = apply(img, news, words)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"
                print("news_paper", img)

            if action == 'GIF':
                obj = gif_filter(img)
                # obj = io.BytesIO(b"")
                # imageio.mimsave(obj, img, 'GIF', duration=0.2)
                # obj=obj.getvalue()
                # obj = io.BytesIO(b"")
                # imageio.mimsave(obj, img, 'GIF', duration=0.2)
                # # Example use ----------------------
                # f2 = open('./media/output/images/output' +
                #             str(instance.id) + '.gif', "wb+")
                # processed_image = request.scheme + "://" + \
                #     request.META["HTTP_HOST"] + \
                #     "/media/output/images/output" + str(instance.id) + ".gif"
                # f2.write(obj.getvalue())
                f2 = open('./media/output/images/output' +
                          str(instance.id) + '.gif', "wb+")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".gif"
                f2.write(obj)


            if action == 'CARTOON':
                img = cartoon_filter(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'SHINEFILTER':
                print('img', img)
                back_black = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]),-1)
                back_shine = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]),-1)
                img = shine_filter(img, back_black,back_shine)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'ROTATE':
                img = filter(img, instance)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'TRIPLE_EXPOSER':
                file2 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
                file3 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]))
                img = triple_exposer(img, file2, file3)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"
            
            if action == 'RED_BLUE':
                img = red_blue(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action=='INVISIBLE_FILTER':
                bg=cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
                img=invisible_filter(img,bg)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action=='DUCK_GIF':
                obj=custom_duck_gif(img,instance)
                print(obj)
                f2 = open('./media/output/images/output' +
                          str(instance.id) + '.gif', "wb+")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".gif"
                f2.write(obj)

            res = img
            if action in ['GIF', 'CLOTH_COLOR_FILTER','DUCK_GIF']:
                instance.processed_image = os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "output.gif")
            else:
                instance.processed_image = os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "output.png")
            processing_file = models.File.objects.get(id=instance.id)
            processing_file.processed_image = processed_image
            processing_file.save()
            hashtag, hashtag_boolean = models.Hashtag.objects.get_or_create(
                name=action)
            print(type(hashtag))
            processed_file_hashtag = models.FileHashtags.objects.create(
                image=processing_file)
            processed_file_hashtag.save()
            processed_file_hashtag.hashtag.add(hashtag)
            processed_file_hashtag.save()
            response = serialize(
                'python', [processing_file], ensure_ascii=False)
            return JsonResponse(response, safe=False)

        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)
            instance_serializer = serializers.FileSerializer(instance)
            file = instance.file.path
            action = request.data['action']
            src = cv2.imread(instance.file.path)
            img = src
            # img=crop_image(img)
            print("img", img)
            if action=='INVISIBLE_FILTER':
                bg=cv2.imread(os.path.join(os.path.abspath(os.path.join(
                    instance.file.path, os.pardir)),'invisible_background.jpg'))
                img=invisible_filter(img,bg)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action=='DUCK_GIF':
                obj=duck_gif(img)
                f2 = open('./media/output/images/output' +
                          str(instance.id) + '.gif', "wb+")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".gif"
                f2.write(obj)

            if action == 'TRIPLE_EXPOSER':
                file2 = cv2.imread(instance.file2.path)
                file3 = cv2.imread(instance.file3.path)
                img = triple_exposer(img, file2, file3)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'FILTER':
                img2 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "pic25.png"))
                img5 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "back.jpg"))
                img = normal_filter(img, img2, img5)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'CARTOON_TEAR':
                back_img = cv2.imread(os.path.join(os.path.abspath(os.path.join(
                    instance.file.path, os.pardir)), "cartoon-snake.png"), -1)
                # img = cartoon_tear(img, back_img)
                inner_img = cv2.imread(os.path.join(os.path.abspath(os.path.join(
                    instance.file.path, os.pardir)), "cartoon-snake-inner.png"), -1)
                img = cartoon_tear(img, back_img, inner_img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'RED_BLUE':
                img = red_blue(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"
                print("red_blue", img)

            if action == 'SHAKING':
                img_back = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "sprit-back.jpg"))
                img = shake_filter(img, img_back)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'TILES':
                tile1 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "tile1.png"), -1)
                tile2 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "tile2.png"), -1)
                tile3 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "tile3.png"), -1)
                tile4 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "tile4.png"), -1)
                tile5 = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "tile5.png"), -1)
                img = tiles_filter(img, tile1, tile2, tile3, tile4, tile5)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'CLOTH_COLOR_FILTER':
                back_img = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "spray-wall.jpg"))
                obj = cloth_color_filter(img, back_img)
                f2 = open('./media/output/images/output' +
                          str(instance.id) + '.gif', "wb+")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".gif"
                f2.write(obj)

            if action == 'SMOKE_FILTER':
                smoke = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "smoke.png"))
                smoke_frame = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "smoke-frame.png"), -1)
                img = smoke_filter(img, smoke, smoke_frame)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'FILTER_MOTIVATION':
                img4 = cv2.imread(
                    (os.path.join(os.path.abspath(os.path.join(
                        instance.file.path, os.pardir)), "motivational.png")),
                    cv2.IMREAD_UNCHANGED)
                img = filter_motivation(img, img4)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"

            if action == 'GIF':
                img = gif_filter(img)
                obj = io.BytesIO(b"")
                imageio.mimsave(obj, img, 'GIF', duration=0.2)
                # Example use ----------------------
                f2 = open('./media/output/images/output' +
                          str(instance.id) + '.gif', "wb+")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".gif"
                f2.write(obj.getvalue())

            if action == 'SHINEFILTER':
                print('img', img)
                back_black = cv2.imread(os.path.join(os.path.abspath(os.path.join(
                    instance.file.path, os.pardir)), "black-face-back.png"), -1)
                back_shine = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "sun-shine-back.png"), -1)
                img = shine_filter(img,back_black,back_shine)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"
                print('imgshine', img)

            if action == 'ROTATE':
                img = filter(img, instance)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"
                print('imgshine', img)

            if action == 'NEWS_PAPER':
                news = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "news.jpeg"))
                words = cv2.imread(os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "words.jpeg"))
                img = apply(img, news, words)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"
                print("news_paper", img)

            if action == 'CARTOON':
                img = cartoon_filter(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = Image.fromarray(img)
                data.save("media/output/images/output" +
                          str(instance.id) + ".png")
                processed_image = request.scheme + "://" + \
                    request.META["HTTP_HOST"] + \
                    "/media/output/images/output" + str(instance.id) + ".png"
                print('imgshine', img)

            res = img
            if action in ['GIF', 'CLOTH_COLOR_FILTER','DUCK_GIF']:
                instance.processed_image = os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "output.gif")
            else:
                instance.processed_image = os.path.join(os.path.abspath(
                    os.path.join(instance.file.path, os.pardir)), "output.png")
            processing_file = models.File.objects.get(id=instance.id)
            processing_file.processed_image = processed_image
            processing_file.save()
            hashtag, hashtag_boolean = models.Hashtag.objects.get_or_create(
                name=action)
            print(type(hashtag))
            processed_file_hashtag = models.FileHashtags.objects.create(
                image=processing_file)
            processed_file_hashtag.save()
            processed_file_hashtag.hashtag.add(hashtag)
            processed_file_hashtag.save()
            response = serialize(
                'python', [processing_file], ensure_ascii=False)
            return JsonResponse(response, safe=False)


class ImageHashtagView(APIView):
    def post(self, request):
        hashtag = request.data.get("hashtag")
        h = models.Hashtag.objects.get(name=hashtag)
        fh = models.FileHashtags.objects.filter(hashtag=h)
        responses = []
        for each in fh:
            img_dict = {
                "file": each.image.file.path,
                "action": each.image.action,
                "timestamp": each.image.timestamp,
                "processed_image": each.image.processed_image
            }
            responses.append(img_dict)
            # responses.append(serialize('python', [img_dict], ensure_ascii=False))
        print(responses)
        return Response(responses)
