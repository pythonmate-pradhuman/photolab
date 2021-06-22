from django.db import models
from users.models import User
import os
import io
import json
import math
import requests

import cartoonize.toonify as toonify
import cv2
import cv2 as cv
import imageio
import imutils
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from file_app.cartoon_filter import cartoon_filter
from file_app.filter_motivation import filter_motivation
from file_app.gif_filter import gif_filter
from file_app.normal_filter import normal_filter
from file_app.rotate_filter import filter
from file_app.shine_filter import shine_filter
from file_app.news_paper import apply
from file_app.red_blue import red_blue
from file_app.shaking import shake_filter
from file_app.tiles import tiles_filter
from django.core.files.base import ContentFile
from file_app.cloth_color import cloth_color_filter
from file_app.smoke import smoke_filter
from file_app.cartoon_tear import cartoon_tear
from file_app.triple_exposer import triple_exposer
from file_app.invisible_filter import invisible_filter
from file_app.duck_gif import custom_duck_gif
from django.core.files.images import ImageFile
# from .views import custom_filter_output
import json
# Create your models here.

ACTION_CHOICES = (
    ('FILTER', 'filter (bg images required:2)'),
    ('FILTER_MOTIVATION', 'filter_motivation (bg images required:1)'),
    ('NEWS_PAPER', 'news_paper (bg images required:2)'),
    ('SHAKING', 'shaking (bg images required:1)'),
    ('TILES', 'tiles (bg images required:5)'),
    ('CLOTH_COLOR_FILTER', 'cloth_color_filter (bg images required:1)'),
    ('SMOKE_FILTER', 'smoke_filter (bg images required:2)'),
    ('CARTOON_TEAR', 'cartoon_tear (bg images required:2)'),
    ('GIF', 'gif (bg images required:0)'),
    ('SHINEFILTER', 'shinefilter (bg images required:2)'),
    ('ROTATE', 'rotate (bg images required:0)'),
    ('CARTOON', 'cartoon (bg images required:0)'),
    ('RED_BLUE', 'red_blue (bg images required:0)'),
    ('TRIPLE_EXPOSER', 'triple_exposer (bg images required:2)'),
    ('INVISIBLE_FILTER','invisible_filter (bg images required : 1)'),
    ('DUCK_GIF','duck_gif bg images reuired:8')
)


def custom_filter_output(instance):
    file = instance.input_file.path
    action = instance.action
    src = cv2.imread(instance.input_file.path)
    img = src

    if action == 'FILTER':
        img2 = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
        img5 = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]))
        img = normal_filter(img, img2, img5)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'CARTOON_TEAR':
        back_img = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]), -1)
        inner_img = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]), -1)
        img = cartoon_tear(img, back_img, inner_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'SHAKING':
        img_back = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
        img = shake_filter(img, img_back)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'TILES':
        tile1 = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]), -1)
        tile2 = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]), -1)
        tile3 = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_3.path, os.pardir)), instance.bg_image_3.name.split("/")[-1]), -1)
        tile4 = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_4.path, os.pardir)), instance.bg_image_4.name.split("/")[-1]), -1)
        tile5 = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_5.path, os.pardir)), instance.bg_image_5.name.split("/")[-1]), -1)
        img = tiles_filter(img, tile1, tile2, tile3, tile4, tile5)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'CLOTH_COLOR_FILTER':
        back_img = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
        obj = cloth_color_filter(img, back_img)

    if action == 'SMOKE_FILTER':
        smoke = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
        smoke_frame = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]), -1)
        img = smoke_filter(img, smoke, smoke_frame)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'FILTER_MOTIVATION':
        img4 = cv2.imread(
            (os.path.join(os.path.abspath(os.path.join(
                instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1])),
            cv2.IMREAD_UNCHANGED)
        img = filter_motivation(img, img4)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'NEWS_PAPER':
        news = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
        words = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]))
        img = apply(img, news, words)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'GIF':
        img = gif_filter(img)
        obj = io.BytesIO(b"")
        imageio.mimsave(obj, img, 'GIF', duration=0.2)
        obj=obj.getvalue()
        # obj = io.BytesIO(b"")
        # imageio.mimsave(obj, img, 'GIF', duration=0.2)
        # # Example use ----------------------
        # f2 = open('./media/output/images/output' +
        #             str(instance.id) + '.gif', "wb+")
        # processed_image = request.scheme + "://" + \
        #     request.META["HTTP_HOST"] + \
        #     "/media/output/images/output" + str(instance.id) + ".gif"
        # f2.write(obj.getvalue())


    if action == 'CARTOON':
        img = cartoon_filter(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'SHINEFILTER':
        print('img', img)
        back_black = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]),-1)
        back_shine = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]),-1)
        img = shine_filter(img, back_black,back_shine)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'ROTATE':
        img = filter(img, instance)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action == 'TRIPLE_EXPOSER':
        file2 = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
        file3 = cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]))
        img = triple_exposer(img, file2, file3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)
    
    if action == 'RED_BLUE':
        img = red_blue(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)

    if action=='INVISIBLE_FILTER':
        bg=cv2.imread(os.path.join(os.path.abspath(
            os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
        img=invisible_filter(img,bg)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = Image.fromarray(img)


    if action=='DUCK_GIF':
        obj=custom_duck_gif(img,instance)
        # print(img)
        # obj = io.BytesIO(b"")
        # imageio.mimsave(obj, img, 'GIF', duration=0.2)
        # obj=obj.getvalue()

    if action in ['CLOTH_COLOR_FILTER','GIF','DUCK_GIF']:
        instance.processed_image.save(instance.input_file.name+'.gif',
                                      ContentFile(obj), save=False)
        instance.perform_save()
    else:
        buf = io.BytesIO()
        data.save(buf, 'PNG')
        instance.processed_image.save(instance.input_file.name,
                                      ContentFile(buf.getvalue()), save=False)
        instance.perform_save()


class CustomFilters(models.Model):
    input_file = models.ImageField(
        upload_to='input/images/', blank=True, null=True)
    name = models.CharField(max_length=50)
    action = models.CharField(max_length=150, choices=ACTION_CHOICES)
    remove_background=models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    bg_image_1 = models.ImageField(
        upload_to='custom/images/', blank=True, null=True)
    bg_image_2 = models.ImageField(
        upload_to='custom/images/', blank=True, null=True)
    bg_image_3 = models.ImageField(
        upload_to='custom/images/', blank=True, null=True)
    bg_image_4 = models.ImageField(
        upload_to='custom/images/', blank=True, null=True)
    bg_image_5 = models.ImageField(
        upload_to='custom/images/', blank=True, null=True)
    bg_image_6 = models.ImageField(
        upload_to='custom/images/', blank=True, null=True)
    bg_image_7 = models.ImageField(
        upload_to='custom/images/', blank=True, null=True)
    bg_image_8 = models.ImageField(
        upload_to='custom/images/', blank=True, null=True)
    # processed_image = models.URLField(blank=True)
    processed_image = models.ImageField(
        upload_to='output/images/', blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "CustomFilters"

    def perform_save(self,*args, **kwargs):
        super(CustomFilters, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.input_file and not self.processed_image:
            super(CustomFilters, self).save(*args, **kwargs)
            instance = CustomFilters.objects.get(id=self.id)
            custom_filter_output(instance=instance)
        elif self.input_file and self.processed_image:
            super(CustomFilters, self).save(*args, **kwargs)
            instance = CustomFilters.objects.get(id=self.id)
            custom_filter_output(instance=instance)
        else:
            super(CustomFilters, self).save(*args, **kwargs)