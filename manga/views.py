from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import Tag, Manga

# Create your views here.

class MangaIndex(ListView):
    model = Manga
    paginate_by = 5
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


class MangaRead(ListView):
    model = Manga
    paginate_by = 1
    template_name = 'manga/manga_reader.html'
    slug_url_kwarg = 'manga_slug'
    context_object_name = 'images'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        manga_slug = self.kwargs['manga_slug']
        queryset = queryset.get(slug=manga_slug)
        images = queryset.images.all()

        return images


class MangaDetail(DetailView):
    model = Manga
    template_name = 'manga/manga_about.html'
    slug_url_kwarg = 'manga_slug'


class MangaAdd(CreateView):
    form_class = MangaAddForm
    template_name = 'manga/manga_add.html'