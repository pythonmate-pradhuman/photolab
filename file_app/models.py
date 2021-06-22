from django.contrib.auth.models import User
import cv2
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .utils import get_filter
import numpy as np
from CustomFilters.models import CustomFilters

ACTION_CHOICES = (
    ('FILTER', 'filter'),
    ('FILTER_MOTIVATION', 'filter_motivation'),
    ('GIF', 'gif'),
    ('SHINEFILTER', 'shinefilter'),
    ('ROTATE', 'rotate'),
    ('CARTOON', 'cartoon'),
    ('NEWS_PAPER', 'news_paper'),
    ('RED_BLUE', 'red_blue'),
    ('SHAKING', 'shaking'),
    ('TILES', 'tiles'),
    ('CLOTH_COLOR_FILTER', 'cloth_color_filter'),
    ('SMOKE_FILTER', 'smoke_filter'),
    ('CARTOON_TEAR', 'cartoon_tear'),
    ('TRIPLE_EXPOSER', 'triple_exposer'),
    ('INVISIBLE_FILTER','invisible_filter'),
    ('DUCK_GIF','duck_gif')
)


class File(models.Model):
    file = models.FileField(upload_to='files')
    file2 = models.FileField(upload_to='files', blank=True, null=True)
    file3 = models.FileField(upload_to='files', blank=True, null=True)
    custom_filter = models.ForeignKey(
        CustomFilters, on_delete=models.CASCADE, blank=True, null=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    processed_image = models.URLField()

    def __str__(self):
        return str(self.id)


class Hashtag(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class FileHashtags(models.Model):
    image = models.OneToOneField(File, on_delete=models.CASCADE)
    hashtag = models.ManyToManyField(Hashtag, blank=True)

    def __str__(self):
        return str(self.id)
