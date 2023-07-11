from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['type']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo']


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'developer', 'get_html_poster', 'get_fans']
    prepopulated_fields = {"slug": ("name", "year")}
    list_filter = ('name', 'platform', 'developer')
    save_on_top = True

    def get_fans(self, object):
        if object.fans.all():
            return [i for i in object.fans.all()]


    def get_html_poster(self, object):
        if object.poster:
            return mark_safe(f"<img src='{object.poster.url}' width=50>")

    get_html_poster.short_description = 'Миниатюра'


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ['user', 'ava']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'game', 'author']


admin.site.site_title = 'Администрация сайта  W.A.S.D'
admin.site.site_header = 'Администрация сайта  W.A.S.D'