from django.contrib import admin
from .models import *
# Register your models here.

class MangaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nsfw', 'author', 'uploader', 'upload_date')
    list_display_links = ('id', 'name')
    list_editable = ('nsfw',)
    search_fields = ('name', 'author', 'uploader')
    list_filter = ('upload_date', 'author', 'uploader', 'nsfw')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'register_date', 'upload_amount', 'comment_amount')
    list_display_links = ('id', 'slug')


class MangaImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'manga')
    search_fields = ('manga',)
    list_filter = ('manga',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'manga', 'profile')
    search_fields = ('manga', 'profile')
    list_filter = ('manga', 'profile')

admin.site.register(Manga, MangaAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(MangaImage, MangaImageAdmin)