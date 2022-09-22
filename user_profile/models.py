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

    def __str__(self):
        return f'{self.user}'
