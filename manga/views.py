from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import Tag, Manga

# Create your views here.

class MangaIndex(ListView):
    model = Manga
    template_name = 'manga/index.html'
    context_object_name = 'mangas'
    
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) |
                                    Q(series__icontains=search_query) |
                                    Q(author__icontains=search_query))
        return queryset


class MangaRead(DetailView):
    model = Manga
    
    template_name = 'manga/manga_reader.html'
    slug_url_kwarg = 'manga_slug'


class MangaDetail(DetailView):
    model = Manga
    template_name = 'manga/manga_about.html'
    slug_url_kwarg = 'manga_slug'



class MangaAdd(CreateView):
    form_class = MangaAddForm
    template_name = 'manga/manga_add.html'