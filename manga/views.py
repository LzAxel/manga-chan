from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Exists, OuterRef, Count


from .forms import *
from .models import *


class MangaIndex(ListView):
    model = Manga
    paginate_by = 5
    template_name = 'manga/index.html'
    context_object_name = 'mangas'
    
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        _search_query = self.request.GET.get('search', None)
        _uploader = self.request.GET.get('uploader', None)

        if _search_query:
            queryset = queryset.filter(Q(name__icontains=_search_query) |
                                    Q(series__icontains=_search_query) |
                                    Q(author__icontains=_search_query))
        
        if _uploader:
            queryset = queryset.filter(uploader__user__username__icontains=_uploader)
        
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(is_liked=Exists(
                Like.objects.filter(
                profile=self.request.user.profile.pk,
                manga=OuterRef('pk'))
            ))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _uploader = self.request.GET.get('uploader', None)

        if _uploader:
            context['title'] = f'Манга залитая пользователем {_uploader}'

        return context


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


class MangaDetail(FormMixin, DetailView):
    model = Manga
    template_name = 'manga/manga_about.html'
    slug_url_kwarg = 'manga_slug'
    context_object_name = 'manga'
    form_class = CommentForm

    def get_success_url(self, *args, **kwargs):
        manga_slug = self.kwargs['manga_slug']

        return reverse_lazy('manga_about', kwargs={'manga_slug': manga_slug})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)

    
    def form_valid(self, form):
        form.instance.manga = self.get_object()
        form.instance.author = self.request.user.profile
        
        form.save()

        return super().form_valid(form)

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
        context['comments'] = manga.get_comments()
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

        return super().form_valid(form)


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'manga/profile.html'
    slug_url_kwarg = 'profile_slug'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['uploaded_manga_amount'] = context['profile'].uploaded_manga.count()
        context['comment_amount'] = context['profile'].comments.count()
        context['liked_manga'] = Manga.objects.filter(likes__profile=context['profile'])
        context['comments'] = context['profile'].get_latest_comments()

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


class Catalog(ListView):
    model = Manga
    template_name = 'manga/catalog.html'
    context_object_name = 'mangas'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.method == 'GET':
            post = self.request.GET
            print("-"*30)
            tags_include = post.getlist('tags_include')
            tags_exclude = post.getlist('tags_exclude')
            status = post.getlist('status')
            print(f"{tags_include=} {tags_exclude=} {status=}")
            if not tags_include:
                queryset = queryset.exclude(tags__slug__in=tags_exclude)
            else:
                queryset = queryset.filter(tags__slug__in=tags_include) \
                    .annotate(num_tags=Count('tags')) \
                    .filter(num_tags=len(tags_include)) \
                    .exclude(tags__slug__in=tags_exclude)
            if status:
                for stat in status:
                    queryset = queryset.filter(**{stat: True})


        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.method == "POST":
            filters = self.request.POST
        context['tags'] = Tag.objects.all()
        print(self.request.POST.getlist('test1'))

        return context
    
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()  
        context = self.get_context_data(*args, **kwargs)
        return self.render_to_response(context)