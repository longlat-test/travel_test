from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Юзер', on_delete=models.CASCADE)
    details = models.CharField(verbose_name='Юзер', max_length=30, default=None)

    class Meta:
        verbose_name = "Пользователь"


# Create your models here.
