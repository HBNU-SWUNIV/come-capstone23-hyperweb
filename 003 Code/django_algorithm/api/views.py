from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
# from .serializers import ItemSerializer
# from .models import Item
from .models import Dog_Info
from .serializers import DogInfoSerializer
import json

import sqlite3
from .calcurate import DietOptimizer
# from calcurate import DietOptimizer

# Create your views here.
# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer


# class FoodViewSet(viewsets.ModelViewSet):
#     queryset = Food_Item.objects.all()
#     serializer_class = FoodItemSerializer

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Dog_Info.objects.all()
    serializer_class = DogInfoSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data_list = []
        for item in serializer.data:
            data = {'dog_mer': item['dog_mer'], 'food_items': item['food_items']}
            min_caloric_val = data['dog_mer']
            print(data['food_items'])
            for food in data['food_items']:
                temp = [food['name'], food['unit']]
                data_list.append(temp)
        
        print(data_list)

        diet_optimizer = DietOptimizer(data_list)
        Food_db = 'db2.sqlite3'
        conn = diet_optimizer.connect_db(Food_db)
        input_list = diet_optimizer.get_input_list(conn, data_list)

        calculated_recipe, nutrients_result = diet_optimizer.calculate_recipe(input_list, min_caloric_val)

        print(calculated_recipe, nutrients_result)
        json_calculated_recipe = json.dumps(calculated_recipe)
        json_nutrients_result = json.dumps(nutrients_result)
        json_result_dict = {
            'calculated_recipe' :  json_calculated_recipe,
            'nutrients_result' : json_nutrients_result
        }
        json_result_list = [json_result_dict]
        print(json_result_list)
        headers = self.get_success_headers(serializer.data)

        return Response(json_result_list, status=status.HTTP_201_CREATED, headers=headers)
    

    # def perform_create(self, serializer):
    #     serializer.save()

