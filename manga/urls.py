from django.urls import path

from .views import * 


urlpatterns = [
    path('', MangaIndex.as_view(), name = "index"),
    path('read/<slug:manga_slug>/', MangaRead.as_view(), name="read"),
    path('manga/<slug:manga_slug>/', MangaDetail.as_view(), name = "manga_about"),
    path('profile/<slug:profile_slug>/', ProfileDetail.as_view(), name = "profile"),
    path('add_manga', MangaAdd.as_view(), name="add_manga"),
    path('login', Login.as_view(), name="login"),
    path('signup', SignUp.as_view(), name="signup"),
    path('logout', user_logout, name='logout'),
    path('like', LikeManga, name='like_manga')
]   