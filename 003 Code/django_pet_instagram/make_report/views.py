from django.shortcuts import render
from make_report.models import Nutrient
from django.http import HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        format, imgstr = request.POST['image_base64'].split(';base64,') 
        ext = format.split('/')[-1] 

        data = ContentFile(base64.b64decode(imgstr))  
        file_name = 'myimage.' + ext  
        file_path = os.path.join('media/', file_name)

        with open(file_path, 'wb') as f:
            f.write(data.read())

        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'fail'}, status=400)
