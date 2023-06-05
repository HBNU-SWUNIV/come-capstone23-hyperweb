from rest_framework import serializers
# from .models import Item
from .models import Food_Item
from .models import Food_save
from .models import Dog_Info
# from .models import Nut_save
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
        
class DogInfoSerializer(serializers.ModelSerializer):
    food_items = FoodItemSerializer(many=True)

    class Meta:
        model = Dog_Info
        fields = ['dog_mer', 'food_items']

    def create(self, validated_data):
        food_items_data = validated_data.pop('food_items')
        dog_info = Dog_Info.objects.create(**validated_data)
        for food_item_data in food_items_data:
            Food_Item.objects.create(dog_info=dog_info, **food_item_data)
        return dog_info

class Food_saveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_save
        fields = '__all__'



# class Nut_saveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Nut_save
#         fields = '__all__'