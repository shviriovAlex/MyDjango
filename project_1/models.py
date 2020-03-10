from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField


class NewsGame(models.Model):
    class Meta:
        db_table = 'post'
        ordering = ["created"]

    STATUS_TYPES = (
        ('private', 'Draft'),
        ('public', 'Published'),
    )
    image = models.ImageField("Изображение")
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_TYPES,
                              default='private')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_materials')
    video = EmbedVideoField(null="True", blank="True", verbose_name="video")
    name_audio = models.CharField(max_length=50, null="True", blank="True")
    audio = models.FileField(name="audio", default="", upload_to="files/", null="True", blank="True")

    def get_absolute_url(self):
        return reverse('project_1:material_details',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(NewsGame, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
