from django.db import models

#from django.contrib.auth.models import User
#from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField
from django.db import models
from django.core.validators import RegexValidator


#AbstractUser._meta.get_field('email')._unique = True
#AbstractUser._meta.get_field('email').blank = False


class MyUserManager(BaseUserManager):
    """

    """
    def create_user(self, email, password, **extra_fields):
        """
        Создаю модель юзера
        """
        if not email:
            raise ValueError('The Email must be set')
        #username = ''
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)





class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile(models.Model):
    SEX_CHOICES = (
        ('m',u"мужской"),
        ('w',u"женский"),
    )
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    name = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
    full_name = models.CharField(verbose_name='Имя и фамилия', max_length=25, default=None, blank=True, null=True)
    user = models.OneToOneField(User, verbose_name='Юзер', on_delete=models.CASCADE)
    sex = models.CharField(max_length=1,verbose_name=u"пол",choices=SEX_CHOICES, default=None, blank=True, null=True)
    status = models.CharField(verbose_name='Статус', max_length=20, default=None, blank=True, null=True)
    place_id = models.CharField(verbose_name='айди города', max_length=100, default=None, blank=True, null=True)
    location = models.CharField(verbose_name='Город', max_length=100, default=None, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='Images', default='Images/None/No-ing.jpg', verbose_name='Изображение')
    background = models.ImageField(upload_to='background', default='Images/None/No-ing.jpg', verbose_name='Задний фон')
    profile_currency = models.CharField(verbose_name='Валюта пользователя', default='USD', max_length=10)
    profile_raiting = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Пользователь"


    def age(self):
        import datetime
        if self.birthday == "Null":

           return int((datetime.date.today() - self.birthday).days / 365.25  )
        else:
           return (0)
    age = property(age)




class Folowers(models.Model):
    users_id = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    folowers_id = models.ManyToManyField(User, related_name='Подписчики', null=True, blank=True)
    folowing_id = models.ManyToManyField(User, related_name='Подписки', null=True, blank=True)

    class Meta:
        verbose_name = "Подписчики/Подписки"
class Tags(models.Model):
    #event_id = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='тег', blank=True, null=True, max_length=30)
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, verbose_name='Автор', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название события', max_length=20)
    image = image = models.ImageField(upload_to='Images/Evenimage', default='Images/None/No-ing.jpg', verbose_name='Изображение события', blank=True, null=True)
    location = models.CharField(verbose_name='Город', max_length=20, default=None, blank=True, null=True)
    budget = models.IntegerField(verbose_name='Бюджет')
    date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    event_raiting = models.IntegerField(default=0)
    balance = MoneyField(max_digits=14, decimal_places=0, default_currency='USD')
    profile_balance = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='теги', null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        verbose_name = "События"

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    hash_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    create_data = models.DateTimeField(blank=True, null=True)


class Comments(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментарий', max_length=50, default=None, blank=True, null=True)
    authors = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)











# Create your models here.
