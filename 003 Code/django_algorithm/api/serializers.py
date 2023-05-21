from rest_framework import serializers
# from .models import Item
from .models import Food_Item

# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = ("__all__")
#         #fields = ('name', 'description', 'cost')


# class FoodItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Food_Item
#         fields = ['name', 'unit']
        
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_Item
        fields = ['name', 'unit']

    def to_internal_value(self, data):
        if isinstance(data, list):  # handle a list of items
            return [super(FoodItemSerializer, self).to_internal_value(item) for item in data]
        else:
            return super(FoodItemSerializer, self).to_internal_value(data)
