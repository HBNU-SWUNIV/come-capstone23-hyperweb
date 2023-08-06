import requests
import random
import base64
import io
import re
import time

from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from user.models import User, Post

import openai
from faker import Faker
from faker.providers import DynamicProvider
from PIL import Image, PngImagePlugin

person_habit_provider = DynamicProvider(
    provider_name="person_habit",
    elements=[
        "독서", "요리", "등산", "서핑", "사진찍기", "그림그리기", "공예", "노래하기",
        "음악감상", "정원가꾸기", "여행", "언어학습", "코딩", "요가", "체스", "수집활동",
        "캠프파이어만들기", "별관측", "글쓰기", "댄스", "낚시", "자전거타기", "조깅", "영화감상",
        "무용", "골프", "스케이트보드", "수영", "마술", "뜨개질", "원예", "유리공예",
        "동물 관찰", "새 관찰", "요리", "도자기", "바둑", "체스", "게임하기", "스노우보드",
        "스케이팅", "복권그리기", "인라인스케이트", "조각하기", "역사 연구", "비행기 조립",
        "로봇 만들기", "드론 조종하기", "양육", "댄스", "비디오 제작", "패션 디자인"
    ]
)

person_profit_provider = DynamicProvider(
    provider_name="person_profit",
    elements=[
        "친절함", "창의성", "정직함", "결단력", "리더십", "배려심", "책임감", "용기", "자기관리",
        "열정", "인내력", "호기심", "긍정성", "적응성", "독립성", "협력심", "타협성", "사려깊음", "신뢰성",
        "상황판단력", "공감능력", "통찰력", "자기통제", "명확한 의사소통", "자기반성", "도전정신", "성실함",
        "팀워크", "지속가능한 발전", "고객 중심", "프로젝트 관리", "문제해결 능력", "전략적 사고"
    ]
)

person_personal_place_provider = DynamicProvider(
    provider_name="person_personal_place",
    elements=[
        "해변", "산", "도서관", "카페", "공원", "박물관", "갤러리", "영화관", "콘서트홀", 
        "스포츠경기장", "요가스튜디오", "쇼핑몰", "정원", "호수", "맛집", "테마파크", "헬스클럽", 
        "휴양지", "사우나", "캠프장", "동물원", "놀이공원", "물놀이공원", "스키장", "게스트하우스",
        "밤시장", "문화센터", "아쿠아리움", "마을", "체험농장", "책방", "클럽", "바", "공연장", "극장"
    ]
)

class Command(BaseCommand):
    def __init__(self):
        self.diffusion_url = "http://127.0.0.1:7860"
        self.set_diffusion_model()
    help = 'Create random users'
    
    def get_gpt_quary1(self):
        system_content = (
            f"I am a system that creates Instagram posts for you."
            f"I don't use emojis based on Unicode characters."
            f"The content I generate includes post captions and hashtags using '#' symbol, output in korean"
        )
        
        assistant_content = (
            f"The content will include details like the user's "
            f"age, gender, hobbies, and the type of dog they have."
        )
        
        user_content = (
            f"person age : {self.user.age}, "
            f"person sex : {self.user.sex}, "
            f"person hobbies : {self.user.personal_habit}, "
            f"person place = {self.user.personal_place}, "
            f"dog type : shiba-inu"
        )
        
        msg = [
            {
                "role": "system",
                "content" : system_content
            },
            {
                "role": "assistant",
                "content": assistant_content
            },
            {
                "role" : "user",
                "content" : user_content
            }
        ]
        return msg
    
    def get_gpt_quary2(self):
        system_content = (
            f"You are an AI model capable of extracting key words and concepts from text content. "
            f"Your task is to analyze an Instagram post and identify the main themes, "
            f"expressed in single words or short phrases. "
            f"Be as precise and concise as possible,you must answered me in English."
        )
        
        user_content = (
            f"I need a compressed word for 10-20 content, please answered me in English"
        )
        
        msg = [
            {
                "role": "system",
                "content" : system_content
                
            },
            {
                "role": "user",
                "content" : user_content
            },
            {
                "role": "user",
                "content": self.gpt_first_response
            }
        ]
        return msg
    
    def get_gpt_prompt(self, msg):
        completion = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo-0613",
                    messages = msg
                    )
        return completion['choices'][0]['message']['content']
    
    def get_gpt_key(self):
        with open('content/management/commands/gpt_key.txt', 'r') as file:
            line = file.read()
        file.close()
        return line
    
    def set_gpt_result(self):
        openai.api_key = self.get_gpt_key()
        self.gpt_first_response = self.get_gpt_prompt(self.get_gpt_quary1())
        print("Log first_prompt : ", self.gpt_first_response)
        self.gpt_second_respose = self.get_gpt_prompt(self.get_gpt_quary2())
        print("Log second_prompt : ", self.gpt_second_respose)
        

    def get_diffusion_quary(self):
        # age, sex, habit, profit, place
        prompt_format = (
            f"person age = {self.user.age}, "
            f"person sex = {self.user.sex}, "
            f"person habit = {self.user.personal_habit}, "
            f"person profit = {self.user.personal_profit}, "
            f"person place = {self.user.personal_place}"
            f"{self.gpt_second_respose}"
        )
        
        negative_prompt_format = (
            f"CyberRealistic_Negative-neg "
        )
        
        payload = {
            "prompt": prompt_format,
            "negative_prompt" : negative_prompt_format,
            "steps": 20,
            "sampler_index": "Euler a",
            "cfg_scale" : 4.5,
            "sampler_name" : "DPM++ SDE Karras",
            "n_iter" : 2
        }
        
        return payload
    
    def set_diffusion_model(self):
        dif_url = f'{self.diffusion_url}/sdapi/v1/options'
        option_payload = {
            "sd_model_checkpoint": "cyberrealistic_v32.safetensors",
            "CLIP_stop_at_last_layers": 2
        }
        response = requests.post(url=dif_url, json=option_payload)
        print(response)
    
    def set_stable_diffusion(self, post):
        dif_url = f"{self.diffusion_url}/sdapi/v1/txt2img"
        print("Log get_diffusion : ",self.get_diffusion_quary())
        response = requests.post(url=dif_url, json=self.get_diffusion_quary())
        img_json = response.json()

        for idx, img in enumerate(img_json['images']):
            # image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            # image.save('output.png')
            img_name = f'{int(time.time())}_{random.randint(1000, 9999)}_{idx}.png'
            
            image = Image.open(io.BytesIO(base64.b64decode(img.split(",", 1)[0])))
            image_io = io.BytesIO()
            image.save(image_io, format='PNG')
            image_file = ContentFile(image_io.getvalue(), name=img_name)

            post.image.save(img_name, image_file)
            
        return post
            
    def handle(self, *args, **kwargs):
        fake = Faker()
        fake_kr = Faker('ko-KR')
        fake_kr.add_provider(person_habit_provider)
        fake_kr.add_provider(person_profit_provider)
        fake_kr.add_provider(person_personal_place_provider)

        def generate_fake_user():
            user = User()
            user.email = fake.email()
            user.age = random.randint(10, 80)
            user.sex = fake.random_element(elements=('Male', 'Female'))
            user.nickname = fake_kr.user_name()
            user.name = fake_kr.name()
            user.set_password(fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True))
            user.is_active = fake.boolean()
            user.is_staff = fake.boolean()
            user.location = fake_kr.city()
            user.company = fake_kr.company()
            user.personal_habit = fake_kr.person_habit()
            user.personal_profit = fake_kr.person_profit()
            user.personal_place = fake_kr.person_personal_place()
        
            user.save()
            
            self.user = user
            post = Post()
            post.user = user
            # gpt quary set
            self.set_gpt_result()
            post.text = self.gpt_first_response
            post.hashtag = re.findall(r'#\w+', self.gpt_first_response)
            
            post = self.set_stable_diffusion(post)
            post.save()

            # image_content = ContentFile(fake.binary(length=(1 * 1)))  # 1MB 이미지 파일 생성
            # image_content.name = 'profile.png'
            # user.profile_image = image_content


        for _ in range(100):  # 10개의 임의의 사용자 생성
            generate_fake_user()
