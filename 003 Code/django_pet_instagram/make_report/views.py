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

from algorithm_api.models import Food_Item, Nut_7_save, Nut_report
from user.models import Dog

import base64
import os


def index(request):
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

class ReportView(APIView):
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
    
        # print('data_food', db_food)
        # print('data_nut7', db_nut7)
        # print('data_nut_report', db_nut_report)
        context = {
            'dog_nickname' : dog_nickname.nickname,
            'foods': db_food,
            'nut7' : db_nut7,
            'nutrients': db_nut_report
        }
            
        return render(request, "report/report2.html", context)

    def post(self, request):
        
        
        
        return render(request, "report/report2.html")


@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        format, imgstr = request.POST['image_base64'].split(';base64,')
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
                resized_tile.save(tile_file_path)

        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'fail'}, status=400)