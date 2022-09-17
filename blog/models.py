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
        related_name='my_posts',
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
    # viewers = models.ManyToManyField(
    #     'auth.User',
    #     through='UserPostRelation',
    #     related_name='view_posts'
    # )

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

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
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['tag_name']


class Comments(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='post_comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='user_comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='replies'
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'{self.author}: {self.text}'


# class UserPostRelation(models.Model):
#
#     RATE_CHOICES = (
#         (1, 'like'),
#         (0, 'neutral'),
#         (-1, 'dislike')
#     )
#
#     user = models.ForeignKey(
#         'auth.User',
#         on_delete=models.CASCADE)
#     post = models.ForeignKey(
#         Post,
#         on_delete=models.CASCADE
#     )
#     rate = models.SmallIntegerField(choices=RATE_CHOICES)
#
#     def __str__(self):
#         return f'{self.user}: {self.post}: {self.rate}'
