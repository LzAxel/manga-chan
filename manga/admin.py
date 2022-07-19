from django.contrib import admin
from .models import *


class MangaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nsfw', 'author', 'uploader', 'upload_date')
    list_display_links = ('id', 'name')
    list_editable = ('nsfw',)
    search_fields = ('name', 'author', 'uploader__user__username')
    list_filter = ('upload_date', 'author', 'uploader', 'nsfw')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'register_date')
    list_display_links = ('id', 'slug')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'manga', 'profile')
    search_fields = ('manga__name', 'profile__user__username')
    list_filter = ('manga', 'profile')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'manga', 'date')
    list_display_links = ('author', 'manga')
    search_fields = ('manga__name', 'author__user__username', 'date')
    list_filter = ('date',)

admin.site.register(Manga, MangaAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)