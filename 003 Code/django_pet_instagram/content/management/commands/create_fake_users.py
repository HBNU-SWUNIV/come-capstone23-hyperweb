import requests
import random
import base64
import io

from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from user.models import User

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
    help = 'Create random users'
    
    def make_json(self):
        # age, sex, habit, profit, place
        prompt_format = (
            f"person age = {self.user.age}, "
            f"person sex = {self.user.sex}, "
            f"person habit = {self.user.personal_habit}, "
            f"person profit = {self.user.personal_profit}, "
            f"person place = {self.user.personal_place}"
            f"one person with one dog"
        )
        payload = {
            "prompt": prompt_format,
            # "negative_prompt" : negative_prompt_format,
            "steps": 20,
            "sampler_index": "Euler a",
        }
        
        return payload
    
    def stable_diffusion(self):
        diffusion_url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
        response = requests.post(diffusion_url, json=self.make_json())
        img_json = response.json()
        
        for i in img_json['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            image.save('output.png')
        

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
            
            self.user = user
            self.stable_diffusion()

            # image_content = ContentFile(fake.binary(length=(1 * 1)))  # 1MB 이미지 파일 생성
            # image_content.name = 'profile.png'
            # user.profile_image = image_content

            user.save()

        for _ in range(100):  # 10개의 임의의 사용자 생성
            generate_fake_user()
