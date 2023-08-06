from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from faker import Faker

from user.models import Dog
from user.models import User
import random

import pandas as pd

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        def get_user_id():
            user_id = User.objects.values_list('id', flat=True)
            return user_id

        def generate_fake_dog(data):
            dog_species = data['영문']
            weight_low = int(data['Weight_low(kg)'])
            weight_high = int(data['Weight_high(kg)'])
            life_span = int(data['Life Span'].split(' ')[2])
            
            db_user_id = get_user_id()

            Dog.objects.create(
                nickname=fake.first_name(),
                species=dog_species,
                age=fake.random_int(min=1, max=life_span),  # 1 ~ 종 평균 max값
                sex=fake.random_element(elements=('0', '1', '2')),  # 중성 암컷 수컷  0 1 2
                weight=random.randint(weight_low, weight_high),  # low ~ high
                activity=fake.random_element(elements=('0', '1', '2', '3', '4')),  # 매우 얌전함,조금 얌전함,보통,조금 활발함,매우 활발함 0 1 2 3 4 
                weight_control=fake.random_int(min=0, max=4),  # 매우 감량, 조금 감량, 유지, 조금 증량, 매우 증량 0 1 2 3 4
                bcs=fake.random_int(min=1, max=9),  # BCS는 1에서 9 사이의 값을 가집니다.
                food_cycle=fake.random_int(min=0, max=3),  # 1주,1달,1년  0 1 2 3
                user_id=random.choice(db_user_id)
            )

        df = pd.read_excel('media/dog_data.xlsx', engine='openpyxl')
        data_list = df.to_dict('records')
        for _ in range(2000):  # 10개의 임의의 사용자 생성
            random_number = random.randint(0, 391)
            generate_fake_dog(data_list[random_number])