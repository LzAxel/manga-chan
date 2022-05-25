from io import BytesIO
from django.db import models
from django.urls import reverse
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
        ("Русский", "Русский"),
        ("Английский", "Английский"),
        ("Японский", "Японский"),
        ("Другой", "Другой")    
    ]
    
    name = models.CharField("Название", max_length=150)
    original_name = models.CharField("Оригинальное Название", max_length=150, blank=True)
    slug = models.SlugField("URL", max_length=255, unique=True, db_index=True)
    description = models.TextField("Описание", default="", blank=True)
    zip = models.FileField("Архив с мангой", upload_to=manga_zip_location, null=False)
    series = models.CharField("Серия", max_length=100)
    author = models.CharField("Автор", max_length=100)
    language = models.CharField("Язык", max_length=100, choices = LANGUAGE_CHOICES)
    tags = models.ManyToManyField("Tag", blank=True, related_name="tagged_manga")
    views = models.IntegerField("Просмотры", default=0, blank=True)
    pages = models.IntegerField("Кол-во страниц", default="0", blank=True)
    uploader = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Кто загрузил")
    upload_date = models.DateTimeField("Дата загрузки", auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="liked_manga", verbose_name="Лайки", blank=True, default=[0])

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('manga_about', kwargs={'manga_slug': self.slug})
    
    def save(self, *args, **kwargs):
        self.pk = Manga.objects.count() + 1
        self.slug = f"{self.pk}-{slugify(self.name)}"
        self.zip.name = f"{self.slug}.zip"
        
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
                # You now have an image which you can save
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


class User(models.Model):
    name = models.CharField("Имя", max_length=30, db_index=True)
    slug = models.SlugField("URL", max_length=255, unique=True, db_index=True)
    register_date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    upload_amount = models.IntegerField("Кол-во добавленных манг", default=0)
    comment_amount = models.IntegerField("Кол-во комментариев", default=0)
    about = models.TextField("О себе")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user', kwargs={'user_slug': self.slug})
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
