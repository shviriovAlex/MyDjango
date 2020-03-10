from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from . import models


# Register your models here.


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


@admin.register(models.MainPage)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'video', 'image')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')

