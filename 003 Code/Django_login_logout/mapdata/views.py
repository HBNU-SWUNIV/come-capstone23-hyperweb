from django.shortcuts import render
from .models import mapdata

def person_list(request):
    mapdata = mapdata.objects.all()
    return render(request, 'mapdata/list.html', {'mapdata': mapdata})