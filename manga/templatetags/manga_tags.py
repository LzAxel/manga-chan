from django import template
from manga.models import Manga, Tag

register = template.Library()

@register.simple_tag(name="get_tags")
def get_manga_tags(manga=None):
    if manga:
        return manga.tags.all()
    else:
        return Tag.objects.all()