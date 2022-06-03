from urllib import request
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.db.models import Exists, OuterRef

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
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(is_liked=Exists(
                Like.objects.filter(
                profile=self.request.user.profile.pk,
                manga=OuterRef('pk'))
            ))
            print("\n"*5,queryset)
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

    def get(self, request, *args, **kwargs):
        obj = Manga.objects.get(slug=kwargs['manga_slug'])
        obj.views += 1
        obj.save(update_fields=('views',))

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            manga = get_object_or_404(Manga, slug=self.kwargs['manga_slug'])
            is_liked = manga.likes.filter(profile=self.request.user.profile).exists()
            context['is_liked'] = is_liked

        return context

class MangaAdd(CreateView):
    form_class = MangaAddForm
    template_name = 'manga/manga_add.html'

    def form_valid(self, form):
        form.instance.uploader = self.request.user.profile
        obj = Profile.objects.get(user=self.request.user)
        obj.upload_amount = Manga.objects.filter(
            uploader=self.request.user.profile).count() + 1
        obj.save(update_fields=('upload_amount',))

        return super().form_valid(form)


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'manga/profile.html'
    slug_url_kwarg = 'profile_slug'


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'manga/signup.html'
    success_url = reverse_lazy('index')


class Login(LoginView):
    form_class = LoginForm
    template_name = 'manga/login.html'

    def get_success_url(self):
        return reverse_lazy('index')

@login_required()
def LikeManga(request):
    manga = get_object_or_404(Manga, pk=request.POST.get('manga_pk'))
    if manga.likes.filter(profile=request.user.profile.pk).exists():
        Like.objects.filter(profile=request.user.profile, manga=manga).delete()
    else:
        Like.objects.create(profile=request.user.profile, manga=manga)

    return redirect(manga.get_absolute_url())


def user_logout(request):
    logout(request)
    return redirect('index')