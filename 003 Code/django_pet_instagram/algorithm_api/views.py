from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response

from .models import FoodList, Monthly_Food, Food_Item, Nut_7_save, Nut_report
from user.models import User, Dog, Dog_Food_Token
from .serializer import MonthItemSerializer, FoodItemSerializer, NutSomeSerializer, Nut7Serializer
from .serializer import Nut_sufficient, NutReportSerializer

import requests
import json

import os
from django.conf import settings
from rest_framework.views import APIView


class Food_view(APIView):
    def __init__(self):
        super().__init__()
        
    def mer_generator(self, age, weight, activate, bcs, sex):
        age, weight, activate, bcs, sex = int(age), int(weight), int(activate), int(bcs), int(sex)
        MER = 132 * (weight ** 0.75)
        coef = 1

        # activte
        if activate > 2:
            coef = coef * 1.06

        #age
        if age > 10:
            coef = coef * 0.8

        #sex
        if sex == 0: # 중성
            coef = coef * 0.75

        #bcs
        if bcs > 4:
            coef = coef * 0.8
        elif bcs > 6:
            coef = coef * 1
        elif bcs > 10:
            coef = coef * 1.2

        calories = MER * coef
        return round(calories)
        
    def json_paser(self, input_result, dog_mer):
        food_dicts = []
        for food_data in input_result:
            food_name = food_data['food']
            food_weight = food_data['weight']  # If you need to use the weight
            food_dicts.append({
                "name": food_name,
                "unit": food_weight  # You can add more fields as necessary
            })
            
        json_list = [{
            "dog_mer" : dog_mer,
            "food_items": food_dicts
        }]
        
        if len(input_result) > 10:
            is_month = True
        else:
            is_month = False
            
        return json_list, is_month
        
    def save_dog_token(self, user, dogs, dog_info_id, is_month):
        dog_token = Dog_Food_Token()
        dog_token.user_id = user
        dog_token.dog_id = dogs
        dog_token.dog_token = dog_info_id
        dog_token.is_month = is_month
        dog_token.save()
        
    #result food month data
    def get_result_month(self, dog_info_id):
        print('result food month info post')
        
        BASE_URL = "http://127.0.0.1:6000/result_month/"
        send_json = {"dog_info_id": dog_info_id}
        
        response = requests.post(BASE_URL, json=send_json)
        serializer = MonthItemSerializer(data=response.json(), many=True)
        
        if serializer.is_valid():
            # Serializer 내부의 create 메소드를 호출하여 저장합니다.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #result food post
    def get_result_food(self, dog_info_id):
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
    
        #result nut some post
    def get_result_nut_some(self, dog_info_id):
        print('result nut some info post')
        
        BASE_URL = "http://127.0.0.1:6000/result_nutsome/"
        send_json = {"dog_info_id": dog_info_id}
        
        response = requests.post(BASE_URL, json=send_json)
        serializer = NutSomeSerializer(data=response.json())
        
        if serializer.is_valid():
            # Serializer 내부의 create 메소드를 호출하여 저장합니다.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    #result nut7 post
    def get_result_nut7(self, dog_info_id):
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
    
        #result nut sufficient post
    def get_result_nut_sufficient(self, dog_info_id):
        print('result nut sufficient info post')
        
        BASE_URL = "http://127.0.0.1:6000/result_nut_sufficient/"
        send_json = {"dog_info_id": dog_info_id}
        
        response = requests.post(BASE_URL, json=send_json)
        serializer = Nut_sufficient(data=response.json())
        
        if serializer.is_valid():
            # Serializer 내부의 create 메소드를 호출하여 저장합니다.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #result nut report post
    def get_result_nut_report(self, dog_info_id):
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


    def get(self, request):
        # login session
        email = request.session.get('email', None)
        user = User.objects.filter(email=email).first()
        dogs = Dog.objects.get(user=user)
        
        request.session['user_id'] = user.id
        request.session['dog_id'] = dogs.id
        request.session['dog_mer'] = self.mer_generator(dogs.age, dogs.weight, dogs.activity, dogs.bcs, dogs.sex)
        print(self.mer_generator(dogs.age, dogs.weight, dogs.activity, dogs.bcs, dogs.sex))
        image_directory = os.path.join(settings.MEDIA_ROOT, 'ingredient_images')
        all_images = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]

        return render(request, "algorithm_api/food_view_ver2.html", {'images': all_images})
  
    
    def post(self, request):
        print('post start')
        print('dogid', request.session.get('dog_id'))
        email = request.session.get('email', None)
        user = User.objects.filter(email=email).first()
        dogs = Dog.objects.get(user=user)
        body_unicode = request.body.decode('utf-8')  # Decode the request body
        body_data = json.loads(body_unicode)  # Parse it into Python dictionary
        input_result = body_data.get('foods')  # Get the foods data

        if not input_result:
            print('Invalid request data')
            return HttpResponseBadRequest("Invalid request data")
        
        json_list, is_month = self.json_paser(input_result, request.session.get('dog_mer'))
        
        print('json_list', json_list)
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
                dog_info_id = result_info['dog_info_id']
                self.save_dog_token(user, dogs, dog_info_id, is_month)
                print('token saved')
                print('end')
                request.session['dog_info_id'] = dog_info_id
                
                if is_month:
                    # get month result
                    response_month = self.get_result_month(dog_info_id)
                    
                    # get daily instance result
                    db_month = Monthly_Food.objects.filter(dog_info=self.dog_info_id).values('food_1', 'food_2', 'food_3', 'food_4')                    
                    first_record = db_month[0]
                    for idx in range(1, 5):
                        instance_dog_id = first_record[f'food_{idx}']
                        # get daily food
                        response_food = self.get_result_food(instance_dog_id)
                        # get daily some nut
                        response_nut_some = self.get_result_nut_some(instance_dog_id)
                        # get daily sufficient nut
                        response_nut_sufficient = self.get_result_nut_sufficient(instance_dog_id)
                    
                    return render(request, 'report/report_month.html')
                
                else:
                    response_food = self.get_result_food(dog_info_id) 
                    # print('log response_food', response_food)

                    response_nut7 = self.get_result_nut7(dog_info_id)
                    # print('log response_nut7', response_nut7)
                    
                    response_nut_report = self.get_result_nut_report(dog_info_id)
                    # print('log response_nut_report', response_nut_report)      

                    return render(request, 'report/report2.html')
            
            
        except requests.RequestException as e:
            # For network exceptions
            print("An error occurred:", str(e))
        return Response(status=400, data=dict(message="음식을 다시 설정하시요."))
