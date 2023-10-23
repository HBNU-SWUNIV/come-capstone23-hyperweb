from rest_framework import serializers

from .models import Monthly_Food, Food_Item, Nut_7_save, Nut_sufficient,  Nut_report

class MonthItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monthly_Food
        fields = ['food_1', 'food_2', 'food_3', 'food_4', 'month_id']
        
    def create(self, validated_data):
        return Monthly_Food.objects.create(**validated_data)
    
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_Item
        fields = ['name', 'unit', 'dog_info']

    def create(self, validated_data):
        return Food_Item.objects.create(**validated_data)
    
class Nut7Serializer(serializers.ModelSerializer):
    class Meta:
        model = Nut_7_save
        fields = ['A10100', 'A10300', 'A10400', 'A10600', 'A10700', 'suffient', 'lack', 'dog_info']
        
    def create(self, validated_data):
        return Nut_7_save.objects.create(**validated_data)
    
class NutSufficientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nut_sufficient
        fields = ['token_name', 'dog_info']
    def create(self, validated_data):
        return Nut_sufficient.objects.create(**validated_data)

class NutReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nut_report
        fields = ['nut_name', 'actual_num', 'percent', 'min_num', 'dog_info']

    def create(self, validated_data):
        return Nut_report.objects.create(**validated_data)
    