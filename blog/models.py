from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=164,
        verbose_name='Url',
        unique=True
    )
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d',
        blank=True
    )
    category = models.ForeignKey(
        'Category',
        related_name='post',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='post',
        blank=True

    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    views = models.IntegerField(
        verbose_name='Просмотры',
        default=0
    )
    likes = models.IntegerField(
        verbose_name='Лайки',
        default=0
    )
    dislikes = models.IntegerField(
        verbose_name='Дизлайки',
        default=0
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-created_date']


class Category(models.Model):
    category_name = models.CharField(
        max_length=128,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=164,
        verbose_name='Url',
        unique=True
    )

    def __str__(self):
        return f'{self.category_name}'

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['category_name']


class Tag(models.Model):
    tag_name = models.CharField(
        max_length=128,
        verbose_name='Тег'
    )
    slug = models.SlugField(
        max_length=164,
        verbose_name='Url',
        unique=True
    )

    def __str__(self):
        return f'{self.tag_name}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['tag_name']
