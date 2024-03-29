from django import forms
from .models import News
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs = {'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs = {'class': 'form-control', 'rows': 5}))
    email = forms.EmailField(label='Получатель', widget=forms.EmailInput(attrs = {'class': 'form-control'}))

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs = {'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs = {'class': 'form-control'}))
    captcha = CaptchaField(label = 'Введите код с картинки')

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs = {'class': 'form-control'}))
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput(attrs = {'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs = {'class': 'form-control'}), help_text='Пароль должен содежрать не менее 8 символов и состоять из букв латинского алфавита и цифр')
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs = {'class': 'form-control'}))
    captcha = CaptchaField(label = 'Введите код с картинки')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'content': forms.Textarea(attrs = {'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs = {'class': 'form-control'})
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'

    
    