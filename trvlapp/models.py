from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model): #профиль 4
    full_name = models.CharField(verbose_name='Имя и фамилия', max_length=25, default=None, blank=True, null=True)
    user = models.OneToOneField(User, verbose_name='Юзер', on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус', max_length=20, default=None, blank=True, null=True)
    location = models.CharField(verbose_name='Город', max_length=20, default=None, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='Images', default='Images/None/No-ing.jpg', verbose_name='Изображение')
    #favorites = models.ManyToManyField(User, related_name='Подписки', null=True)
    folowing_id = models.ManyToManyField(User, related_name='Подписка', null=True, blank=True)
    #folowers_id = folowing_id # профили 1, 2, 3
    class Meta:
        verbose_name = "Пользователь"

    def age(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25  )
    age = property(age)

class Folowers(models.Model):
    users_id = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    folowers_id = models.ManyToManyField(User, related_name='Подписчики', null=True)

    class Meta:
        verbose_name = "Пользователь"




# Create your models here.
