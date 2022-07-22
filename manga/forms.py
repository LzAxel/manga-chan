from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *


class MangaAddForm(forms.ModelForm):
    required_css_class = "add-manga__required"
    
    class Meta:
        model = Manga
        fields = ['name', 'original_name', 'description', 'series',
                    'author', 'language', 'tags', 'zip', 'nsfw']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input--inner',
                                            'placeholder': 'Название'}),
            'original_name': forms.TextInput(attrs={'class': 'input input--inner',
                                            'placeholder': 'Оригинальное Название'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'rows': 5,
                                            'placeholder': 'Описание'}),
            'series': forms.TextInput(attrs={'class': 'input input--inner',
                                            'placeholder': 'Серия'}),
            'author': forms.TextInput(attrs={'class': 'input input--inner',
                                            'placeholder': 'Автор манги'}),
            'language': forms.Select(attrs={'class': 'input input--inner'}),
            'tags': forms.SelectMultiple(attrs={'class': 'select'}),
            'nsfw': forms.CheckboxInput(attrs={'class': 'check-box'}),
            'zip': forms.FileInput(attrs={'class': 'file'})
        }


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'input input--inner', 'placeholder': 'Логин'}
    ))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'input input--inner', 'placeholder': 'Пароль'}
    ))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'class': 'input input--inner', 'placeholder': 'Повторите пароль'}
    ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password1')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'input input--inner', 'placeholder': 'Логин'}
    ))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'input input--inner', 'placeholder': 'Пароль'}
    ))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'textarea',
                                            'name': 'text', 'cols':'15', 'rows':'6'}),
        }