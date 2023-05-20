from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
# from .serializers import ItemSerializer
# from .models import Item
from .models import Food_Item
from .serializers import FoodItemSerializer
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
    queryset = Food_Item.objects.all()
    serializer_class = FoodItemSerializer

    def create(self, request):
        # if isinstance(request.data, list):  # handle a list of items
        #     serializer = self.get_serializer(data=request.data, many=True)
        # else:
        #     serializer = self.get_serializer(data=request.data)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)

        # DietOptimizer(data_list)
        queryset = Food_Item.objects.all()
        data_list = []
        for item in queryset:
            data = {'name': item.name, 'unit': item.unit}
            temp = [data['name'], data['unit']]
            data_list.append(temp)
        print(data_list)
        diet_optimizer = DietOptimizer(data_list)
        Food_db = 'db2.sqlite3'
        conn = diet_optimizer.connect_db(Food_db)
        input_list = diet_optimizer.get_input_list(conn, data_list)
        for i in input_list:
            print(i)
        calculated_recipe, nutrients_result = diet_optimizer.calculate_recipe(input_list)

        print(calculated_recipe, nutrients_result)

        headers = self.get_success_headers(serializer.data)

        return Response(calculated_recipe, status=status.HTTP_201_CREATED, headers=headers)
    

    # def perform_create(self, serializer):
    #     serializer.save()

