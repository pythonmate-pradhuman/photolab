from .models import CustomFilters
from .serializers import CustomFiltersSerializer
from django.shortcuts import render
import cv2
import os
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
from file_app.cloth_color import cloth_color_filter
from file_app.smoke import smoke_filter
from file_app.cartoon_tear import cartoon_tear
import io
from django.core.files.base import ContentFile
from rest_framework import generics, viewsets
# Create your views here.


class CustomFiltersViewset(viewsets.ModelViewSet):
    queryset = CustomFilters.objects.all()
    serializer_class = CustomFiltersSerializer


# def custom_filter_output(instance):
#     file = instance.input_file.path
#     action = instance.action
#     src = cv2.imread(instance.input_file.path)
#     img = src
#     print("img", img)
#     if action == 'FILTER':
#         img2 = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
#         img5 = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]))
#         img = normal_filter(img, img2, img5)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         data = Image.fromarray(img)

#     if action == 'CARTOON_TEAR':
#         back_img = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]), -1)
#         img = cartoon_tear(img, back_img)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         data = Image.fromarray(img)

#     if action == 'SHAKING':
#         img_back = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
#         img = shake_filter(img, img_back)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         data = Image.fromarray(img)

#     if action == 'TILES':
#         tile1 = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]), -1)
#         tile2 = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]), -1)
#         tile3 = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_3.path, os.pardir)), instance.bg_image_3.name.split("/")[-1]), -1)
#         tile4 = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_4.path, os.pardir)), instance.bg_image_4.name.split("/")[-1]), -1)
#         tile5 = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_5.path, os.pardir)), instance.bg_image_5.name.split("/")[-1]), -1)
#         img = tiles_filter(img, tile1, tile2, tile3, tile4, tile5)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         data = Image.fromarray(img)

#     if action == 'CLOTH_COLOR_FILTER':
#         back_img = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
#         obj = cloth_color_filter(img, back_img)

#     if action == 'SMOKE_FILTER':
#         smoke = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
#         smoke_frame = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]), -1)
#         img = smoke_filter(img, smoke, smoke_frame)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         data = Image.fromarray(img)

#     if action == 'FILTER_MOTIVATION':
#         img4 = cv2.imread(
#             (os.path.join(os.path.abspath(os.path.join(
#                 instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1])),
#             cv2.IMREAD_UNCHANGED)
#         img = filter_motivation(img, img4)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         data = Image.fromarray(img)

#     if action == 'NEWS_PAPER':
#         news = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_1.path, os.pardir)), instance.bg_image_1.name.split("/")[-1]))
#         words = cv2.imread(os.path.join(os.path.abspath(
#             os.path.join(instance.bg_image_2.path, os.pardir)), instance.bg_image_2.name.split("/")[-1]))
#         img = apply(img, news, words)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         data = Image.fromarray(img)
#     if action == 'CLOTH_COLOR_FILTER':
#         print("CLOTH_COLOR_FILTER")
#         instance.processed_image.save(instance.input_file.name+'.gif',
#                                       ContentFile(obj), save=False)
#         instance.save()
#     else:
#         buf = io.BytesIO()
#         data.save(buf, 'PNG')
#         instance.processed_image.save(instance.input_file.name,
#                                       ContentFile(buf.getvalue()), save=False)
#         instance.save()
