from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Exists, OuterRef

from .forms import *
from .models import *


class MangaIndex(ListView):
    model = Manga
    paginate_by = 5
    template_name = 'manga/index.html'
    context_object_name = 'mangas'
    
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        search_query = self.request.GET.get('search', None)
        uploader = self.request.GET.get('uploader', None)
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) |
                                    Q(series__icontains=search_query) |
                                    Q(author__icontains=search_query))
        
        if uploader:
            queryset = queryset.filter(uploader__user__username__icontains=uploader)
        
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(is_liked=Exists(
                Like.objects.filter(
                profile=self.request.user.profile.pk,
                manga=OuterRef('pk'))
            ))

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
    context_object_name = 'manga'

    def get_object(self):
        manga_slug = self.kwargs.get('manga_slug')
        manga = get_object_or_404(Manga, slug=manga_slug)
        manga.views = manga.views + 1
        manga.save(update_fields=('views',))

        return manga
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manga = context['manga']
        context['preview'] = manga.images.first().image.url
        user = self.request.user
        if user.is_authenticated:
            is_liked = manga.likes.filter(profile=user.profile).exists()
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
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['uploaded_manga_amount'] = context['profile'].uploaded_manga.count()
        context['liked_manga'] = Manga.objects.filter(likes__profile=context['profile'])
        print(context['liked_manga'])

        return context


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