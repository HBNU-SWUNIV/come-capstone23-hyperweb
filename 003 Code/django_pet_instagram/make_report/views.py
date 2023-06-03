from django.shortcuts import render
from make_report.models import Nutrient
from django.http import HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import math
from PIL import Image

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

# @csrf_exempt
# def save_image(request):
#     if request.method == 'POST':
#         format, imgstr = request.POST['image_base64'].split(';base64,') 
#         ext = format.split('/')[-1] 

#         data = ContentFile(base64.b64decode(imgstr))  
#         file_name = 'myimage.' + ext  
#         file_path = os.path.join('media/', file_name)

#         with open(file_path, 'wb') as f:
#             f.write(data.read())

#         return JsonResponse({'status': 'success'}, status=200)
#     else:
#         return JsonResponse({'status': 'fail'}, status=400)


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