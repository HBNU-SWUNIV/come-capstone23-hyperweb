from django.core.management.base import BaseCommand
from faker import Faker
from user.models import User, Post  # 앱 이름을 사용해 모델을 import 해야합니다.
import random

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fake = Faker()

        def get_user_id():
            
            return int(random.random()*100)

        def generate_fake_post(user_id):
            Post.objects.create(
                user_id=user_id,
                text=fake.text(),  # 임의의 텍스트 생성
                hashtag=fake.word(),  # 임의의 단어 생성
            )

        db_user_id = 1
        for _ in range(200):  # 2000개의 임의의 포스트 생성
            # random_user_id = random.choice(db_user_id)
            generate_fake_post(1)
