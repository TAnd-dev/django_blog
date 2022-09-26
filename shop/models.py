from django.db import models
from django.db import models
from django.urls import reverse
from mptt.fields import TreeManyToManyField
from mptt.models import MPTTModel, TreeForeignKey


def upload_product_photo(instance, filename):
    return f'shop/{instance.salesman.pk}/{filename}'


class Category(MPTTModel):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=64
    )
    slug = models.SlugField(
        max_length=164,
        verbose_name='Url',
        unique=False
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product_category', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=164,
        verbose_name='Url',
        unique=True
    )
    salesman = models.ForeignKey(
        'auth.User',
        verbose_name='Продавец',
        related_name='salesman',
        on_delete=models.CASCADE
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.FloatField(
        verbose_name='Цена',
        default=0
    )
    photo = models.ImageField(
        upload_to=upload_product_photo,
        blank=True
    )
    category = TreeManyToManyField(
        Category,
        verbose_name='Категория'
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

#
