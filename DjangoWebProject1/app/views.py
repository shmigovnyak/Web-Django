"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import FeedbackForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Blog, Comment
from .forms import BlogForm
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required




def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ссылки',
            'message':'',
            'year':datetime.now().year,
        }
    )

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            feature_labels = {
                "design": "Дизайн",
                "usability": "Удобство",
                "content": "Контент",
                "speed": "Скорость работы"
            }
            liked_features_text = [feature_labels[feature] for feature in data.get('liked_features', [])]

            response_data = {
                "success": True,
                "name": data["name"],
                "email": data["email"],
                "rating": data["rating"],
                "liked_features": liked_features_text,
                "suggestions": data["suggestions"]
            }
            return JsonResponse(response_data)

        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    form = FeedbackForm()
    return render(request, "app/pool.html", {'title': 'Обратная связь', "form": form, 'year': datetime.now().year})

def registration(request):
    """Renders the registration page."""
    
    assert isinstance(request, HttpRequest)

    if request.method == "POST":  # После отправки формы
        regform = UserCreationForm(request.POST)

        if regform.is_valid():  # Валидация полей формы
            reg_f = regform.save(commit=False)  # Не сохраняем автоматически данные формы
            reg_f.is_staff = False  # Запрещен вход в административный раздел
            reg_f.is_active = True  # Активный пользователь
            reg_f.is_superuser = False  # Не является суперпользователем
            reg_f.date_joined = datetime.now()  # Дата регистрации
            reg_f.last_login = datetime.now()  # Дата последней авторизации
            reg_f.save()  # Сохраняем изменения после добавления данных

            return redirect('home')  # Переадресация на главную страницу после регистрации

    else:
        regform = UserCreationForm()  # Создание объекта формы для ввода данных нового пользователя

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # Передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )
 

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Рецепты',
            'posts': posts,
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    # Получаем статью по ID
    post = get_object_or_404(Blog, id=parametr)
    
    # Получаем все комментарии к статье, отсортированные по дате
    comments = Comment.objects.filter(post=post).order_by('-date')
    
    # Обработка формы для добавления комментария
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                # Сохраняем комментарий, добавляем недостающие данные
                comment_f = form.save(commit=False)
                comment_f.author = request.user
                comment_f.date = datetime.now()
                comment_f.post = post
                comment_f.save()
                return redirect('blogpost', parametr=post.id)
        else:
            form = CommentForm()  # Если пользователь не авторизован, форма не отправляется
    else:
        form = CommentForm()  # Пустая форма для нового комментария
    
    return render(request, 'app/blogpost.html', {
        
        'title': 'Рецепты',
        'post': post,
        'comments': comments,
        'form': form,
        'year':datetime.now().year,
    })


@login_required
def newpost(request):
    if not request.user.is_superuser:
        return redirect('blog')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Используем форму!
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogForm()  # Создаём пустую форму

    return render(request, 'app/newpost.html', {'form': form,  'year':datetime.now().year})


def video(request):
    return render (request, 'app/video_page.html',{'year':datetime.now().year})