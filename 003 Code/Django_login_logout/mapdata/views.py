from django.shortcuts import render
from .models import Mapdata
from .serializers import MapDataSerializer
import json

def map(request):
    datas = Mapdata.objects.all()[:100] # 100개로 제한
    serializer = MapDataSerializer(datas, many=True)
    context = {'map_data': serializer.data}
    return render(request, 'mapdata/list.html', context)


def map_list(request, n):
    datas = Mapdata.objects.all()[n]
    latlon = {
        'lat': datas.latitude,
        'lon': datas.longitude,
        'place' : datas.place
    }
    latlonJson = json.dumps(latlon)
    return render(request, 'mapdata/mapviewer.html', {'latlonJson': latlonJson})