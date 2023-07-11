from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *


class GameForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['platform'].empty_label = 'Платформа не выбрана'
        self.fields['developer'].empty_label = 'Разработчик не выбран'

    class Meta:
        model = Game
        exclude = ['views', 'slug', 'fans']

    def clean_name(self): # собственный валидатор
        name = self.cleaned_data['name']
        if 'qarasuv' == name:
            raise ValidationError('Название не должно содержать имя \'qarasuv\'')
        return name

class PlatformForm(ModelForm):
    class Meta:
        model = Platform
        fields = '__all__' # все поля кроме автоматических


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class DeveloperForm(ModelForm):
    class Meta:
        model = Developer
        fields = '__all__'

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Enter your login"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': "Enter your Password"}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': "Return your Password"}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Enter your login"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'placeholder': "Оставьте ваши пожелания!"}))
    captcha = CaptchaField()