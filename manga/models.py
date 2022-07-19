from io import BytesIO
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from pytils.translit import slugify
from zipfile import ZipFile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Create your models here.

def manga_zip_location(self, zipname):
    return f'manga/{self.slug}/{zipname}'

def manga_image_location(self, zipname):
    return f'manga/{self.manga.slug}/{zipname}'


class Comment(models.Model):
    text = models.TextField('Текст', blank=False, null=False)
    manga = models.ForeignKey('Manga', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return f"{self.author.user.username} - {self.manga.name} - {self.text}"
   
    def get_manga(self):
        return self.manga
    

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-date"]

class MangaImage(models.Model):
    manga = models.ForeignKey("Manga", models.CASCADE, "images", verbose_name="Манга")
    image = models.ImageField('Фото', upload_to=manga_image_location, blank=True)
    
    def __str__(self):
        return self.manga.name


class Manga(models.Model):
    LANGUAGE_CHOICES = [
        (None, "Выберите язык"),
        ("Русский", "Русский"),
        ("Английский", "Английский"),
        ("Японский", "Японский"),
        ("Другой", "Другой")    
    ]
    
    name = models.CharField("Название", max_length=150)
    original_name = models.CharField("Оригинальное Название", max_length=150, blank=True)
    slug = models.SlugField("URL", max_length=255, unique=True, db_index=True)
    description = models.TextField("Описание", default="", blank=True)
    zip = models.FileField("Архив с мангой", upload_to=manga_zip_location, null=False, blank=True)
    series = models.CharField("Серия", max_length=100)
    author = models.CharField("Автор", max_length=100)
    language = models.CharField("Язык", max_length=100, choices = LANGUAGE_CHOICES)
    tags = models.ManyToManyField("Tag", blank=True, related_name="tagged_manga")
    views = models.IntegerField("Просмотры", default=0, blank=True)
    pages = models.IntegerField("Кол-во страниц", default=0, blank=True)
    uploader = models.ForeignKey("Profile", on_delete=models.CASCADE, verbose_name="Кто загрузил", related_name="uploaded_manga")
    upload_date = models.DateTimeField("Дата загрузки", auto_now_add=True)
    nsfw = models.BooleanField("NSFW", default=False, null=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('manga_about', kwargs={'manga_slug': self.slug})
    
    def get_likes_count(self):
        return self.likes.count()
    
    def get_preview(self):
        return self.images.all()[0].image.url
    
    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                self.pk = Manga.objects.latest("pk").pk + 1
            except:
                self.pk = 1

        self.slug = f"{self.pk}-{slugify(self.name)}"
        self.zip.name = f"{self.pk}-{self.slug}.zip"
        try:
            this = Manga.objects.get(pk=self.pk)
            
            if this.zip.url:
                self.zip = this.zip
                super(Manga, self).save(*args, **kwargs)
        except:
            if self.zip:
                extansions = ['png', 'jpg', 'webp', 'jpeg', 'gif']
                zip_file = ZipFile(self.zip)
                files = sorted(zip_file.namelist(), key=lambda x: x.lstrip("0"))
                self.pages = len([i.split('.')[-1] for i in files if i.split('.')[-1] in extansions])
                super(Manga, self).save(*args, **kwargs)
                for num, name in enumerate(files):
                    data = zip_file.read(name)
                    try:
                        from PIL import Image
                        image = Image.open(BytesIO(data))
                        image.load()
                        image = Image.open(BytesIO(data))
                        image.verify()
                    except ImportError:
                        pass
                    except:
                        continue
                    name = f"{num}.{name.split('.')[-1]}"
                    print(name)

                    path = manga_zip_location(self, name)
                    saved_path = default_storage.save(path, ContentFile(data))
                    self.images.create(image=saved_path)
    
    def get_comments(self):
        return self.comments.all()

    class Meta:
        verbose_name = "Манга"
        verbose_name_plural = "Манги"
        ordering = ["-upload_date"]


class Tag(models.Model):
    name = models.CharField("Название", max_length=30)
    slug = models.SlugField("URL", max_length=255, unique=True, db_index=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name',]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField("URL", max_length=255, unique=True, db_index=True)
    image = models.ImageField("Фотография профиля", null=True, blank=True)
    register_date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    about = models.TextField("О себе")

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            slug = slugify(instance.username)
            Profile.objects.create(user=instance, slug=slug)
    
    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        try:
            instance.profile.save()
        except:
            slug = slugify(instance.username)
            Profile.objects.create(user=instance, slug=slug)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_slug': self.slug})
    
    def get_latest_comments(self, count=10):
        return self.comments.all()[:count]
    
    def get_avatar(self):
        if self.image:
            return self.image.url
        else:
            return """data:image/png;base64,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"""


    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Like(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE, 'liked_manga', verbose_name='Профиль')
    manga = models.ForeignKey(Manga, models.CASCADE, 'likes', verbose_name='Манга')

    def __str__(self):
        return f"{self.profile.user.username} - {self.manga.name}"
    
    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"