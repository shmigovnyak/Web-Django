from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # Добавляем изображение

    def get_absolute_url(self):
        return reverse('blogpost', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ['-posted']

# Регистрируем в админке
from django.contrib import admin
admin.site.register(Blog)


class Comment(models.Model):
    # Структура модели для комментариев
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Комментарий от {self.author.username} к {self.post.title}"