from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def upload_profile_photo(instance, filename):
    return f'profiles/{instance.user.pk}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    profile_pic = models.ImageField(
        upload_to=upload_profile_photo,
        null=True,
        blank=True
    )
    tel = models.IntegerField(
        verbose_name='Телефон',
        null=True,
        blank=True
    )
    country = models.CharField(
        max_length=24,
        verbose_name='Страна',
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=32,
        verbose_name='Город',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user}'
