from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Dog(models.Model):
    nickname = models.CharField(max_length=30, default="")
    species = models.CharField(max_length=30)
    age = models.IntegerField()
    sex = models.CharField(max_length=10) # 0 1 2
    weight = models.CharField(max_length=30)
    activity = models.CharField(max_length=100) # 0 1 2 3 4
    weight_control = models.IntegerField() # 0 1 2 3 4순
    bcs = models.IntegerField()
    food_cycle = models.IntegerField(default=0) # 0-> 없음 1 -> 1주 2-> 1달 3 -> 1년
    improve = models.CharField(max_length=30, blank=True)
    disease = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.species} - {self.age} - {self.sex}"

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=254)
    nickname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(upload_to='profile_images', default='default_profile.png')
    location = models.CharField(default="", max_length=30, blank=True)
    company = models.CharField(default="", max_length=30, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'name']

    objects = MyUserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return self.email

    


    