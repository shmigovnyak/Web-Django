"""
Definition of forms.
"""

from django import forms
from .models import Comment
from .models import Blog
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User 
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя", 
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-controld', 'placeholder': 'Введите ваше имя'})
    )
    email = forms.EmailField(
        label="Ваш email", 
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-controld', 'placeholder': 'Введите ваш email'})
    )
    rating = forms.ChoiceField(
        label="Оцените сайт",
        choices=[(1, "1 - Плохо"), (2, "2 - Средне"), (3, "3 - Хорошо"), (4, "4 - Отлично"), (5, "5 - Превосходно")],
        widget=forms.RadioSelect(attrs={'class': 'form-radio'}),
        required=True,
    )
    liked_features = forms.MultipleChoiceField(
        label="Что вам понравилось?",
        choices=[
            ("design", "Дизайн"), 
            ("usability", "Удобство"), 
            ("content", "Контент"), 
            ("speed", "Скорость работы")
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        required=False
    )
    suggestions = forms.CharField(
        label="Ваши пожелания",
        widget=forms.Textarea(attrs={"class": "form-textarea", "rows": 4, "cols": 40, "placeholder": "Введите ваши пожелания"}),
        required=False
    )
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': ""}
        

class BlogForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Выберите автора",
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Автор" 
    )

    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image', 'author')
        labels = {
            'title': "Заголовок",
            'description': "Краткое содержание",
            'content': "Полное содержание",
            'image': "Изображение",
            'author': "Автор"
        }