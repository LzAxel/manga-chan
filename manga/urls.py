from django.urls import path

from .views import * 


urlpatterns = [
    path('', MangaIndex.as_view(), name = "index"),
    path('read/<slug:manga_slug>/', MangaRead.as_view(), name="read"),
    path('manga/<slug:manga_slug>/', MangaDetail.as_view(), name = "manga_about"),
    path('add_manga', MangaAdd.as_view(), name="add_manga")
]   