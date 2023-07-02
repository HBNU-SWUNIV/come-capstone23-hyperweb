from rest_framework import serializers

from .models import Food_Item, Nut_7_save, Nut_report

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

class NutReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nut_report
        fields = ['nut_name', 'actual_num', 'percent', 'min_num', 'dog_info']

    def create(self, validated_data):
        return Nut_report.objects.create(**validated_data)
    