from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth.decorators import login_required

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
    SEX_CHOICES = [
        (0, '중성'),
        (1, '암컷'),
        (2, '수컷'),
    ]

    ACTIVITY_CHOICES = [
        (0, '매우 얌전함'),
        (1, '조금 얌전함'),
        (2, '보통'),
        (3, '조금 활발함'),
        (4, '매우 활발함'),
    ]

    WEIGHT_CONTROL_CHOICES = [
        (0, '매우 감량'),
        (1, '조금 감량'),
        (2, '유지'),
        (3, '조금 증량'),
        (4, '매우 증량'),
    ]

    FOOD_CYCLE_CHOICES = [
        (0, '없음'),
        (1, '1주'),
        (2, '1달'),
        (3, '1년'),
    ]

    nickname = models.CharField(max_length=30, default="")
    species = models.CharField(max_length=30)
    age = models.IntegerField()
    weight = models.CharField(max_length=30)
    bcs = models.IntegerField()
    improve = models.CharField(max_length=30, blank=True)
    disease = models.CharField(max_length=30, blank=True)
    sex = models.IntegerField(choices=SEX_CHOICES)
    activity = models.IntegerField(choices=ACTIVITY_CHOICES)
    weight_control = models.IntegerField(choices=WEIGHT_CONTROL_CHOICES)
    food_cycle = models.IntegerField(choices=FOOD_CYCLE_CHOICES, default=0)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        # return f"{self.species} - {self.age} - {self.sex}"
        return f"{self.age} - {self.weight} - {self.activity} - {self.bcs} - {self.sex}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=254)
    age = models.IntegerField(default=20, blank=True)
    sex = models.CharField(default="Male", max_length=10, blank=True)
    nickname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(upload_to='profile_images', default='default_profile.png')
    location = models.CharField(default="", max_length=30, blank=True)
    company = models.CharField(default="", max_length=30, blank=True)
    personal_habit = models.CharField(default="", max_length=30, blank=True)
    personal_profit = models.CharField(default="", max_length=30, blank=True)
    personal_place = models.CharField(default="", max_length=30, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'name']

    objects = MyUserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return self.email
    
class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    hashtag = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.text

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/posts/images', blank=True, null=True)

    def __str__(self):
        return self.post.text + " Image"


class Dog_Food_Token(models.Model):
    user_id = models.ForeignKey(User, related_name='Dog_food_token', on_delete=models.CASCADE, null=True)
    dog_id = models.ForeignKey(Dog, related_name='Dog_food_token', on_delete=models.CASCADE, null=True)
    dog_token = models.IntegerField()
    is_month = models.BooleanField()
    
    def __str__(self):
        return self.dog_token