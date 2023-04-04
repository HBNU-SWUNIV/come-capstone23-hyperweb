from rest_framework.serializers import ModelSerializer
from .models import Mapdata

class MapDataSerializer(ModelSerializer):
    class Meta:
        model = Mapdata
        fields = '__all__'