from django.contrib import admin
from .models import Manga, MangaImage, Profile, Tag
# Register your models here.

class MangaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nsfw', 'author', 'uploader', 'upload_date')
    list_display_links = ('id', 'name')
    list_editable = ('nsfw',)
    search_fields = ('name', 'author', 'uploader')
    list_filter = ('upload_date', 'author', 'uploader')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'register_date', 'upload_amount', 'comment_amount')
    list_display_links = ('id', 'slug')


admin.site.register(Manga, MangaAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(MangaImage)