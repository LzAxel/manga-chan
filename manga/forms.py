from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *


class MangaAddForm(forms.ModelForm):
    required_css_class = "add-manga__required"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Manga
        fields = ['name', 'original_name', 'description', 'series',
                    'author', 'language', 'tags', 'zip', 'nsfw']
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
            'nsfw': forms.CheckboxInput(attrs={'class': 'check__input'}),
            'zip': forms.FileInput(attrs={'class': 'form__file'})
        }


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Логин'}
    ))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form__input', 'placeholder': 'Пароль'}
    ))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'class': 'form__input', 'placeholder': 'Повторите пароль'}
    ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password1')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Логин'}
    ))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form__input', 'placeholder': 'Пароль'}
    ))