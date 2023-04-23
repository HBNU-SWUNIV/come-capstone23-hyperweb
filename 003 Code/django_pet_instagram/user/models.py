from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import hashlib

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

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=254)
    nickname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    species = models.CharField(max_length=30)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    weight = models.CharField(max_length=30)
    activity = models.CharField(max_length=100)
    weight_control = models.CharField(max_length=30)
    bcs = models.IntegerField()
    cycle = models.CharField(max_length=30, blank=True)
    improve = models.CharField(max_length=30, blank=True)
    disease = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(upload_to='profile_images', default='/media/default_profile.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'name', 'species', 'age', 'sex', 'weight', 'activity', 'weight_control', 'bcs']

    objects = MyUserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return self.email
    