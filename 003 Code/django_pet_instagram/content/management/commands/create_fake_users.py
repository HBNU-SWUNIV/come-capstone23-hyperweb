from django.core.management.base import BaseCommand
from user.models import User
import random
from faker import Faker
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Create random users'

    def handle(self, *args, **kwargs):
        fake = Faker()

        def generate_fake_user():
            user = User()
            user.email = fake.email()
            user.nickname = fake.user_name()
            user.name = fake.name()
            user.set_password(fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True))
            user.is_active = fake.boolean()
            user.is_staff = fake.boolean()
            user.location = fake.city()
            user.company = fake.company()

            image_content = ContentFile(fake.binary(length=(1024 * 1024)))  # 1MB 이미지 파일 생성
            image_content.name = 'profile.png'
            user.profile_image = image_content

            user.save()

        for _ in range(10):  # 10개의 임의의 사용자 생성
            generate_fake_user()
