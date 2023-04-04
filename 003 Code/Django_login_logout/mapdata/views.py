from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Mapdata
from .serializers import MapDataSerializer


@api_view(['GET'])
def map(request):
    datas = Mapdata.objects.all()[:100] # 100개로 제한
    serializer = MapDataSerializer(datas, many=True)
    return Response(serializer.data)