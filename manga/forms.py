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
                    'author', 'language', 'tags', 'uploader', 'zip', 'nsfw']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input',
                                            'placeholder': 'Название'}),
            'original_name': forms.TextInput(attrs={'class': 'form__input',
                                            'placeholder': 'Оригинальное Название'}),
            'description': forms.Textarea(attrs={'class': 'form__input', 'rows': 5,
                                            'placeholder': 'Описание'}),
            'series': forms.TextInput(attrs={'class': 'form__input',
                                            'placeholder': 'Серия'}),
            'author': forms.TextInput(attrs={'class': 'form__input',
                                            'placeholder': 'Автор манги'}),
            'language': forms.Select(attrs={'class': 'form__input'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form__input'}),
            'uploader': forms.Select(attrs={'class': 'form__input'}),
            'nsfw': forms.CheckboxInput(attrs={'class': 'check__input'}),
            'zip': forms.FileInput(attrs={'class': 'form__file'})
        }