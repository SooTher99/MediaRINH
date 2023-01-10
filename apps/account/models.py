from django.db import models
from utils.validators import FileMimeValidator
from django.contrib.auth.models import AbstractUser


def upload_to(instance, filename):
    return f'users/avatars/{filename}'


class User(AbstractUser):
    # Кастомные поля
    post_agreement = models.BooleanField('Соглашение на рассылку', default=True)
    avatar = models.ImageField('Аватарка', upload_to=upload_to, blank=True, null=True, validators=[FileMimeValidator()])

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

