"""
Definition of urls for DjangoWebProject1.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import views, forms  
from datetime import datetime

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('links/', views.links, name='links'),
    path('feedback/', views.feedback_view, name='feedback'),
    path(
        'login/',
        LoginView.as_view(
            template_name='app/login.html',
            authentication_form=forms.BootstrapAuthenticationForm,
            extra_context={
                'title': 'Авторизация',
                'year': datetime.now().year,
            }
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('registration/', views.registration, name='registration'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost/', views.newpost, name='newpost'),  # Должно быть views.newpost
    path('video/', views.video, name='video'),
]

# Добавляем поддержку медиа-файлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
