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
import os

from pathlib import Path
from django.conf import settings
# Create your models here.

def manga_zip_location(self, zipname):
    return f'manga/{self.slug}/{zipname}'

def manga_image_location(self, zipname):
    return f'manga/{self.manga.slug}/{zipname}'



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
    pages = models.IntegerField("Кол-во страниц", default="0", blank=True)
    uploader = models.ForeignKey("Profile", on_delete=models.CASCADE, verbose_name="Кто загрузил")
    upload_date = models.DateTimeField("Дата загрузки", auto_now_add=True)
    likes = models.ManyToManyField("Profile", related_name="liked_manga", verbose_name="Лайки", blank=True, default=[0])
    nsfw = models.BooleanField("NSFW", default=False, null=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('manga_about', kwargs={'manga_slug': self.slug})
    
    def get_likes_count(self):
        return self.likes.count()
    
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
    register_date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    upload_amount = models.IntegerField("Кол-во добавленных манг", default=0)
    comment_amount = models.IntegerField("Кол-во комментариев", default=0)
    about = models.TextField("О себе")

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            slug = slugify(instance.username)
            Profile.objects.create(user=instance, slug=slug)
    
    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_slug': self.slug})
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
