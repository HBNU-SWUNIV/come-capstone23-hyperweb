from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response

from .models import FoodList, Food_Item, Nut_7_save, Nut_report
from user.models import User, Dog, Dog_Food_Token
from .serializer import FoodItemSerializer, Nut7Serializer, NutReportSerializer

import requests
import json

import os
from django.conf import settings
from rest_framework.views import APIView

#result food get
def result_food(dog_info_id):
    print('result food info post')
    
    BASE_URL = "http://127.0.0.1:6000/result_food/"
    send_json = {"dog_info_id": dog_info_id}
    
    response = requests.post(BASE_URL, json=send_json)
    serializer = FoodItemSerializer(data=response.json(), many=True)
    
    if serializer.is_valid():
        # Serializer 내부의 create 메소드를 호출하여 저장합니다.
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#result nut7 post
def result_nut7(dog_info_id):
    print('result nut7 info post')
    
    BASE_URL = "http://127.0.0.1:6000/result_nut7/"
    send_json = {"dog_info_id": dog_info_id}
    
    response = requests.post(BASE_URL, json=send_json)
    serializer = Nut7Serializer(data=response.json())
    
    if serializer.is_valid():
        # Serializer 내부의 create 메소드를 호출하여 저장합니다.
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#result nut report post
def result_nut_report(dog_info_id):
    print('result nut report info post')
    
    BASE_URL = "http://127.0.0.1:6000/result_nut_report/"
    send_json = {"dog_info_id": dog_info_id}
    
    response = requests.post(BASE_URL, json=send_json)
    serializer = NutReportSerializer(data=response.json(), many=True)
    
    if serializer.is_valid():
        # Serializer 내부의 create 메소드를 호출하여 저장합니다.
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def caloric_generator(age, weight, activate, bcs, sex):
    cal_weight =  1
    # weight = 15

    MER = 132 * (weight ** 0.75)

    if activate == 0:
        cal_weight = cal_weight * 0.75
    elif activate == 1:
        cal_weight = cal_weight * 0.90
    elif activate == 2:
        cal_weight = cal_weight * 1.06
    elif activate == 3:
        cal_weight = cal_weight * 1.21
    elif activate == 4:
        cal_weight = cal_weight * 1.36
    
    if age == 0:
        cal_weight = cal_weight * 1.4
    elif age == 1:
        cal_weight = cal_weight * 1.2
    elif age > 10:
        cal_weight = cal_weight * 0.8

    if sex == 0:
        cal_weight = cal_weight * 0.8

    if bcs > 4:
        cal_weight = cal_weight * 0.8
    elif bcs > 6:
        cal_weight = cal_weight * 1
    elif bcs > 10:
        cal_weight = cal_weight * 1.2

    calories = MER * cal_weight
    return round(calories)


class Food_view(APIView):
    def __init__(self):
        super().__init__()
        self.dog_mer = 0
        self.age = 10
        self.weight = 12
        self.activate = 2
        self.bcs = 4
        self.sex = 0
        self.user = None
        self.dog = None
        self.dog_info_id = None
        self.dog_id = None

    def get(self, request):
        # login session
        email = request.session.get('email', None)
        user = User.objects.filter(email=email).first()
        user = User.objects.get(email=email)
        dogs = Dog.objects.get(user=user)     
        self.user = user
        self.dog = dogs
        self.dog_id = dogs.id
        request.session['dog_id'] = dogs.id

        image_directory = os.path.join(settings.MEDIA_ROOT, 'ingredient_images')
        all_images = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]

        return render(request, "algorithm_api/food_view_ver2.html", {'images': all_images})
  
    
    
    def post(self, request):
        
        print('post start')
        body_unicode = request.body.decode('utf-8')  # Decode the request body
        body_data = json.loads(body_unicode)  # Parse it into Python dictionary
        input_result = body_data.get('foods')  # Get the foods data

        if not input_result:
            print('Invalid request data')
            return HttpResponseBadRequest("Invalid request data")

        # food_list_model = FoodList()
        # food_list_model.save()
        food_dicts = []
        for food_data in input_result:
            food_name = food_data['food']
            food_weight = food_data['weight']  # If you need to use the weight
    
            food_dict = {
                "name": food_name,
                "unit": food_weight  # You can add more fields as necessary
            }
            food_dicts.append(food_dict)

        dog_mer = self.dog_mer
        json_dict = {
            "dog_mer" : dog_mer,
            "food_items": food_dicts
        }
        json_list = [json_dict]

        BASE_URL = "http://127.0.0.1:6000/Food_Item/"
        try:
            # POST request
            response = requests.post(BASE_URL, json=json_list)
            # print(response)
            if response.status_code == 205:
                return Response(status=205, data=dict(message="음식을 다시 설정하시요."))
            else:
                result_info = response.json()
                print(result_info['dog_info_id'])
                self.dog_info_id = result_info['dog_info_id']
                dog_token = Dog_Food_Token()
                dog_token.user_id = self.user
                dog_token.dog_id = self.dog
                dog_token.dog_token = self.dog_info_id
                dog_token.save()
                print('token saved')
                print('end')
                request.session['dog_info_id'] = self.dog_info_id
                
                response_food = result_food(self.dog_info_id) 
                # print('log response_food', response_food)

                response_nut7 = result_nut7(self.dog_info_id)
                # print('log response_nut7', response_nut7)
                
                response_nut_report = result_nut_report(self.dog_info_id)
                # print('log response_nut_report', response_nut_report)      

                return render(request, 'report/report2.html')
            
            
            
        except requests.RequestException as e:
            # For network exceptions
            print("An error occurred:", str(e))
        return Response(status=400, data=dict(message="음식을 다시 설정하시요."))
