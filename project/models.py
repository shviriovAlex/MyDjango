from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField


class ObjectsWithScoresManager(object):
    pass


class MainPage(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            default="")
    publish = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    video = EmbedVideoField(null="True", blank="True", verbose_name="video")
    name_audio = models.CharField(max_length=50, null="True", blank="True")
    audio = models.FileField(name="audio", default="", null="True", blank="True")
    objects = models.Manager()
    image = models.ImageField("Изображение", default="")

    def get_absolute_url(self):
        return reverse('project:material',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


# Create your models here.

