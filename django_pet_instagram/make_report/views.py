from django.shortcuts import render
from make_report.models import Nutrient
from django.http import HttpResponse


def index(request):
    nutrients = Nutrient.objects.all()
    context = {
        'nutrients': nutrients
    }
    return render(request, 'report/report3.html', context)


def make_report(request):
    nutrients = Nutrient.objects.all()
    context = {
        'nutrients': nutrients
    }
    return render(request, 'report.html', context)