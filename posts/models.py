import datetime as dt

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group, blank=True, null=True,
        on_delete=models.SET_NULL, related_name='posts'
    )
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        text_start = self.text[:20]
        text_end = self.text[-20:-1]
        author = self.author
        date = dt.datetime.strftime(self.pub_date, '%d-%m-%Y')

        return (
            f'Автор: {author}, '
            f'Дата: {date}, '
            f'Фрагмент текста: {text_start}.....{text_end}'
        )

    class Meta:
        ordering = (['-pub_date'])
