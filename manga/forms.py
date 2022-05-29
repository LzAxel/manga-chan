from django import forms
from .models import *


class MangaAddForm(forms.ModelForm):
    required_css_class = "add-manga__required"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].empty_label = 'Не выбран'
    
    class Meta:
        model = Manga
        fields = ['name', 'original_name', 'description', 'series',
                    'author', 'language', 'tags', 'uploader', 'zip']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'manga-form__input',
                                            'placeholder': 'Название'}),
            'original_name': forms.TextInput(attrs={'class': 'manga-form__input',
                                            'placeholder': 'Оригинальное Название'}),
            'description': forms.Textarea(attrs={'class': 'manga-form__input', 'rows': 5,
                                            'placeholder': 'Описание'}),
            'series': forms.TextInput(attrs={'class': 'manga-form__input',
                                            'placeholder': 'Серия'}),
            'author': forms.TextInput(attrs={'class': 'manga-form__input',
                                            'placeholder': 'Автор манги'}),
            'language': forms.Select(attrs={'class': 'manga-form__input'}),
            'tags': forms.SelectMultiple(attrs={'class': 'manga-form__input'}),
            'uploader': forms.Select(attrs={'class': 'manga-form__input'}),
            'zip': forms.FileInput(attrs={'class': 'manga-form__file'})
        }