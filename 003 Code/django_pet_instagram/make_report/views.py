from django.shortcuts import render
from make_report.models import Nutrient
from django.http import HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import JsonResponse

from rest_framework.views import APIView

import math
from PIL import Image

from algorithm_api.models import Monthly_Food, Food_Item, Nut_7_save, Nut_report, Nut_sufficient
from user.models import User, Dog

import base64
import os

def report_month(request):
    # 예제 데이터 (실제 데이터로 교체하셔야 합니다.)
    weekly_meals = {
        'food_1': {
            'menu': ['돼지고기', '감자', '브로콜리','연두부'],
            'features': ['칼슘이 풍부한', '단백질이 풍부한', '나트륨이 풍부한'],
            'color': 'rgba(255,0,0,0.3)',
            'days': ['1', '22', '3', '4', '5', '23', '7'],
        },
        'food_2': {
            'menu': ['소고기', '고구마', '달걀'],
            'features': ['비타민C가 풍부한', '단백질이 풍부한', '지방이 풍부한'],
            'color': 'rgba(0, 0, 255, 0.3)',  # 블루 색상의 투명도를 0.3으로 설정
            'days': ['8', '16', '10', '11', '20', '21', '14','31'],
        },
        'food_3': {
            'menu': ['닭고기', '파프리카','감자', '고구마'],
            'features': ['지방이 풍부한', '탄수화물이 풍부한', '비타민B가 풍부한'],
            'color': 'lightgreen',
            'days': ['15', '9', '17', '18', '19', '25', '13','30'],
        },
        'food_4': {
            'menu': ['소고기', '감자', '옥수수','귀리'],
            'features': ['단백질이 풍부한', '나트륨이 풍부한', '지방이 풍부한'],
            'color': 'lightyellow',
            'days': ['2', '6', '24', '12', '26', '27', '28','29'],
        },
    }
    calcium_data = {
        'food_1': 83,
        'food_2': 17,
        'food_3': 94,
        'food_4': 42
    }
    magnesium_data = {
        'food_1': 28,
        'food_2': 55,
        'food_3': 74,
        'food_4': 9
    }
    iron_data = {
        'food_1': 66,
        'food_2': 38,
        'food_3': 90,
        'food_4': 51
    }
    month_days = [
        ['1', '2', '3', '4', '5', '6', '7'],
        ['8', '9', '10', '11', '12', '13', '14'],
        ['15', '16', '17', '18', '19', '20', '21'],
        ['22', '23', '24', '25', '26', '27', '28'],
        ['29','30','31']
    ]

    
    return render(request, 'report/report_month.html', {
        'weekly_meals': weekly_meals,
        'calcium_data': calcium_data,
        'magnesium_data': magnesium_data,
        'iron_data': iron_data,
        'month_days': month_days
    })
    
class Report2(APIView):
    def get(self, request):
        nutrients = Nutrient.objects.all()
        context = {
            'nutrients': nutrients
        }
        return render(request, 'report/report2.html', context)

def make_report(request):
    nutrients = Nutrient.objects.all()
    context = {
        'nutrients': nutrients
    }
    return render(request, 'report.html', context)

class ReportMonthView(APIView):
    def __init__(self):
        super().__init__()
        self.dog_info_id = None
        self.dog_id = None
    
    def get(self, request):
        self.dog_info_id = request.session.get('dog_info_id')
        self.dog_id = request.session.get('dog_id')
        month_id = request.session.get('month_id')
        print(self.dog_id)
        dog_nickname = Dog.objects.get(id=self.dog_id)
        print('report dog info: ', self.dog_info_id, 'dog_nickname', dog_nickname)
        
        foods_list = []
        token_list = []
        some_nut_list = []
        db_month = Monthly_Food.objects.filter(month_id=month_id).values('food_1', 'food_2', 'food_3', 'food_4')
        print(db_month)
        first_record = db_month[0]
        
        # 음식 재료, 음식에 대한 특징, nut7, 
        
        
        for idx in range(1, 5):
            dog_id = first_record[f'food_{idx}']
            
            db_food = Food_Item.objects.filter(dog_info=dog_id).values('name')
            print(db_food)
            foods = []
            for food in db_food:
                foods.append(food)
            foods_list.append(foods)
            
            db_token = Nut_sufficient.objects.filter(dog_info=dog_id).values('token_name')
            tokens = []
            for token in db_token:
                tokens.append(token)
            token_list.append(tokens)
            
            db_some_nut = Nut_7_save.objects.filter(dog_info=dog_id).values('A10300', 'A10400', 'A10600')
            print(db_some_nut)
            somes = []
            for some in db_some_nut:
                somes.append(some)
            some_nut_list.append(somes)

        
        calcium_data = {
            'food_1': db_some_nut[0][0],
            'food_2': db_some_nut[1][0],
            'food_3': db_some_nut[2][0],
            'food_4': db_some_nut[3][0]
        }
        magnesium_data = {
            'food_1': db_some_nut[0][1],
            'food_2': db_some_nut[1][1],
            'food_3': db_some_nut[2][1],
            'food_4': db_some_nut[3][1]
        }
        iron_data = {
            'food_1': db_some_nut[0][2],
            'food_2': db_some_nut[1][2],
            'food_3': db_some_nut[2][2],
            'food_4': db_some_nut[3][2]
        }
        
        weekly_meals = {
            'food_1': {
                'menu': foods_list[0],
                'features': token_list[0],
                'color': 'rgba(255,0,0,0.3)',
                'days': ['1', '22', '3', '4', '5', '23', '7'],
            },
            'food_2': {
                'menu': foods_list[1],
                'features': token_list[1],
                'color': 'rgba(0, 0, 255, 0.3)',  # 블루 색상의 투명도를 0.3으로 설정
                'days': ['8', '16', '10', '11', '20', '21', '14','31'],
            },
            'food_3': {
                'menu': foods_list[2],
                'features': token_list[2],
                'color': 'lightgreen',
                'days': ['15', '9', '17', '18', '19', '25', '13','30'],
            },
            'food_4': {
                'menu': foods_list[3],
                'features': token_list[3],
                'color': 'lightyellow',
                'days': ['2', '6', '24', '12', '26', '27', '28','29'],
            },
        }
        
        month_days = [
            ['1', '2', '3', '4', '5', '6', '7'],
            ['8', '9', '10', '11', '12', '13', '14'],
            ['15', '16', '17', '18', '19', '20', '21'],
            ['22', '23', '24', '25', '26', '27', '28'],
            ['29','30','31']
        ]

        context = {
            'weekly_meals': weekly_meals,
            'calcium_data': calcium_data,
            'magnesium_data': magnesium_data,
            'iron_data': iron_data,
            'month_days': month_days
        }
            
        return render(request, "report/report_month.html", context)

    def post(self, request):
        
        return render(request, "report/report_month.html")

class ReportView2(APIView):
    def __init__(self):
        super().__init__()
        self.dog_info_id = None
        self.dog_id = None
    
    def get(self, request):
        self.dog_info_id = request.session.get('dog_info_id')
        self.dog_id = request.session.get('dog_id')
        print(self.dog_id)
        dog_nickname = Dog.objects.get(id=self.dog_id)
        print('report dog info: ', self.dog_info_id, 'dog_nickname', dog_nickname)
        db_food = Food_Item.objects.filter(dog_info=self.dog_info_id).values('name', 'unit')
        
        db_nut7 = Nut_7_save.objects.get(dog_info=self.dog_info_id)
        # fields_nut7 = ['A10100', 'A10300', 'A10400', 'A10600', 'A10700', 'suffient', 'lack']
        
        db_nut_report = Nut_report.objects.filter(dog_info=self.dog_info_id).values('nut_name', 'actual_num', 'percent', 'min_num')
        # fields_nut_report = ['nut_name', 'actual_num', 'percent', 'min_num']
        
        db_nut_sufficient = Nut_sufficient.objects.filter(dog_info=self.dog_info_id).values('token_name')
        # fields_nut_report = ['nut_name', 'actual_num', 'percent', 'min_num']
        print(db_nut_sufficient)
        
        
        nutrients = [
            "에너지", "수분", "단백질", "지방", "탄수화물", "칼슘", "철", "마그네슘", "인", "칼륨",
            "나트륨", "아연", "구리", "망간", "셀레늄", "요오드", "비타민 A", "티아민", "리보플라빈", "니아신",
            "판토텐산", "피리독신", "엽산_엽산당량", "비타민 B12", "비타민 D", "비타민 E", "비타민 K", "이소류신",
            "류신", "라이신", "메티오닌", "페닐알라닌", "트레오닌", "트립토판", "발린", "히스티딘", "아르기닌",
            "리놀레산", "알파 리놀렌산"
        ]
        
        unit_df = [
            "A10100", "A10200", "A10300", "A10400", "A10600",
            "B10100", "B10200", "B10300", "B10400", "B10500",
            "B10600", "B10700", "B10800", "B10900", "B11000",
            "B11200", "C10100", "C20100", "C20200", "C20300",
            "C20500", "C20601", "C20900", "C21200", "C10200",
            "C10300", "C10400", "D10201", "D10202", "D10203",
            "D10204", "D10205", "D10206", "D10207", "D10208",
            "D10209", "D10210", "E10601", "E10602"
        ]

        code_to_nutreints = dict(zip(unit_df,nutrients))
        db_nut_sufficient_code_to_nut = [code_to_nutreints[item['token_name']] for item in db_nut_sufficient]


        # print('data_food', db_food)
        # print('data_nut7', db_nut7)
        # print('data_nut_report', db_nut_report)
        context = {
            'dog_nickname' : dog_nickname.nickname,
            'foods': db_food,
            'nut7' : db_nut7,
            'nutrients': db_nut_report,
            'sufficient': db_nut_sufficient_code_to_nut
        }
            
        return render(request, "report/report2.html", context)

    def post(self, request):
        
        return render(request, "report/report2.html")
    
@csrf_exempt
def report_to_post(request):
    if request.method == 'POST':
        # 이미지 저장
        format, imgstr = request.POST['images'].split(';base64,')
        ext = format.split('/')[-1]

        # Decode base64 image data and save it as a file
        data = ContentFile(base64.b64decode(imgstr))
        file_name = 'myimage.' + ext
        file_path = os.path.join('media/', file_name)

        with open(file_path, 'wb') as f:
            f.write(data.read())

        # Open the saved image file
        image = Image.open(file_path)

        # Check if the image height is larger than 1080
        if image.height > 1080:
            # Calculate the number of tiles needed to fit the image vertically
            num_tiles = math.ceil(image.height / 1080)
            request.session['post_image_num'] = num_tiles
            for i in range(num_tiles):
                # Calculate the coordinates of the tile
                upper = int(i * 1080)
                lower = int((i + 1) * 1080)

                # Crop the tile from the image
                tile = image.crop((0, upper, image.width, lower))

                # Resize the tile to 1920x1080
                resized_tile = tile.resize((1920, 1080))

                # Save the resized tile
                tile_file_path = os.path.join('media/', f'tile_{i}_{file_name}')
                request.session[f'post_image{i}'] = tile_file_path
                resized_tile.save(tile_file_path)

        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'fail'}, status=400)
        
@csrf_exempt
def save_image(request):
    return
#     if request.method == 'POST':
#         format, imgstr = request.POST['image_base64'].split(';base64,')
#         ext = format.split('/')[-1]

#         # Decode base64 image data and save it as a file
#         data = ContentFile(base64.b64decode(imgstr))
#         file_name = 'myimage.' + ext
#         file_path = os.path.join('media/', file_name)

#         with open(file_path, 'wb') as f:
#             f.write(data.read())

#         # Open the saved image file
#         image = Image.open(file_path)

#         # Check if the image height is larger than 1080
#         if image.height > 1080:
#             # Calculate the number of tiles needed to fit the image vertically
#             num_tiles = math.ceil(image.height / 1080)

#             for i in range(num_tiles):
#                 # Calculate the coordinates of the tile
#                 upper = int(i * 1080)
#                 lower = int((i + 1) * 1080)

#                 # Crop the tile from the image
#                 tile = image.crop((0, upper, image.width, lower))

#                 # Resize the tile to 1920x1080
#                 resized_tile = tile.resize((1920, 1080))

#                 # Save the resized tile
#                 tile_file_path = os.path.join('media/', f'tile_{i}_{file_name}')
#                 resized_tile.save(tile_file_path)

#         return JsonResponse({'status': 'success'}, status=200)
#     else:
#         return JsonResponse({'status': 'fail'}, status=400)