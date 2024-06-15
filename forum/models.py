from django.db import models
from django.urls import reverse


def upload_forum_photo(instance, filename):
    return f'forum/{instance.pk}/{filename}'


class ThemeForum(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='Название темы',
    )
    author = models.ForeignKey(
        'auth.User',
        verbose_name='Автор',
        related_name='author',
        on_delete=models.CASCADE
    )
    slug = models.SlugField(
        max_length=64,
        verbose_name='url',
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    photo = models.ImageField(
        upload_to=upload_forum_photo,
        blank=True,
        null=True,
    )
    created_date = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('theme_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_date',]


class CommentForum(models.Model):
    theme = models.ForeignKey(
        ThemeForum,
        verbose_name='Тема',
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'auth.User',
        verbose_name='Автор',
        related_name='forum_comments',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_date = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        ordering = ['-created_date',]

