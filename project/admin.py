from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from . import models


# Register your models here.


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


# admin.site.register(models.Comment)


@admin.register(models.NewsGame)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'publish', 'video')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'body')  # добавляем поиск
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(models.MainPage)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'video', 'image')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Games)
class ProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.OldGames)
class ProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
