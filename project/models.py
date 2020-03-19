from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
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
    audio = models.FileField(name="audio", default="", upload_to="files/", null="True", blank="True")
    objects = models.Manager()
    image = models.ImageField("Изображение", upload_to="image/", default="")

    def get_absolute_url(self):
        return reverse('project:material',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class NewsGame(models.Model):
    class Meta:
        db_table = 'post'
        ordering = ["created"]

    STATUS_TYPES = (
        ('private', 'Draft'),
        ('public', 'Published'),
    )
    image = models.ImageField("Изображение")
    image2 = models.ImageField("Изображение1")
    image3 = models.ImageField("Изображение2")
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
        return reverse('project:material_details',
                       args=[self.publish.year,
                             self.publish.month,
                             self.slug])

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to="user/", blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    user_like = models.ManyToManyField(NewsGame,
                                       related_name='user_likes')

    def __str__(self):
        return "Profile for {}".format(self.user.username)


class Comment(models.Model):
    author_comment = models.OneToOneField(settings.AUTH_USER_MODEL,
                                          on_delete=models.CASCADE,
                                          default=True)
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



# Create your models here.
