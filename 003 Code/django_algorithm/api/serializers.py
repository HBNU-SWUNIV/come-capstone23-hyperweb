from rest_framework import serializers

from .models import Food_Item, Monthly_Food, Dog_Info, Get_Id, Nut_some_save, Nut_7_save, Nut_report, Nut_sufficient


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_Item
        fields = ['name', 'unit', 'dog_info']
        
class MonthItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monthly_Food
        fields = ['foods', 'dog_info']

class NutSomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nut_some_save
        fields = ['B10100', 'B10300', 'B10700', 'dog_info']
        
class Nut7Serializer(serializers.ModelSerializer):
    class Meta:
        model = Nut_7_save
        fields = ['A10100', 'A10300', 'A10400', 'A10600', 'A10700', 'suffient', 'lack', 'dog_info']
        
class NutSufficientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nut_sufficient
        fields = ['token_name', 'dog_info']

class NutReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nut_report
        fields = ['nut_name', 'actual_num', 'percent', 'min_num', 'dog_info']
        
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
    
class GetIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Get_Id
        fields = ['dog_info_id']
        