from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.core.files.base import ContentFile

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response

from .models import Monthly_Food, Food_Item, Nut_7_save, Nut_report, Food_image, Food_Item_En
from user.models import User, Dog, Dog_Food_Token
from .serializer import MonthItemSerializer, FoodItemSerializer, Nut7Serializer
from .serializer import NutSufficientSerializer, NutReportSerializer, FoodItemEnSerializer

import requests
import json
import time, random

import base64
import io

from PIL import Image, PngImagePlugin

import os
from django.conf import settings
from rest_framework.views import APIView


class Food_view(APIView):
    def __init__(self):
        super().__init__()
        self.diffusion_url = "http://127.0.0.1:7860"
        
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
        
    def get_diffusion_quary(self, en_food):
        # age, sex, habit, profit, place
        prompt_format = (            
            f"RAW photo, (dog food made with {' and '.join(en_food)})"
            f"<lora:foodphoto:0.8> foodphoto, dslr, soft lighting, high quality, film grain, Fujifilm XT"

        )
        
        negative_prompt_format = (
            f"(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4),"
            f"(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, "
            f"mutation, mutated, ugly, disgusting, amputation "
        )
        
        payload = {
            "prompt": prompt_format,
            "negative_prompt" : negative_prompt_format,
            "steps": 20,
            "cfg_scale" : 7,
            "sampler_name" : "Euler a",
            "n_iter" : 1
        }
        
        return payload
    
    def set_diffusion_model(self):
        dif_url = f'{self.diffusion_url}/sdapi/v1/options'
        option_payload = {
            "sd_model_checkpoint": "realisticVisionV51_v51VAE.safetensors",
            "CLIP_stop_at_last_layers": 2
        }
        response = requests.post(url=dif_url, json=option_payload)
        print(response)
        
    #result food month data
    def get_result_month(self, month_id):
        print('result food month info post')
        
        BASE_URL = "http://127.0.0.1:6000/result_month/"
        send_json = {"month_id": month_id}
        
        response = requests.post(BASE_URL, json=send_json)
        serializer = MonthItemSerializer(data=response.json())
        
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

    #result food en version
    def get_result_food_en(self, dog_info_id):
        print('result food info post en')
        
        BASE_URL = "http://127.0.0.1:6000/result_food_en/"
        send_json = {"dog_info_id": dog_info_id}
        
        response = requests.post(BASE_URL, json=send_json)
        serializer = FoodItemEnSerializer(data=response.json(), many=True)
        # db_Food_en = Food_Item_En.objects.filter(dog_info=dog_info_id).values('name')
        food_en_list = [item['name'].replace("(", "").replace(")", "").replace("'", "").strip() for item in response.json()]

        print('db_Food_en', food_en_list)
            
        self.set_diffusion_model()
        print("Log get_diffusion : ",self.get_diffusion_quary(food_en_list))
        
        dif_url = f"{self.diffusion_url}/sdapi/v1/txt2img"
        response = requests.post(url=dif_url, json=self.get_diffusion_quary(food_en_list))
        img_json = response.json()
        
        for idx, img in enumerate(img_json['images']):
            # image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            # image.save('output.png')
            img_name = f'{int(time.time())}_{random.randint(1000, 9999)}_{idx}.png'
            
            image = Image.open(io.BytesIO(base64.b64decode(img.split(",", 1)[0])))
            image_io = io.BytesIO()
            image.save(image_io, format='PNG')
            image_file = ContentFile(image_io.getvalue(), name=img_name)
            
            post_image = Food_image(dog_info=dog_info_id, image=image_file)
            post_image.save()
        
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
        serializer = NutSufficientSerializer(data=response.json(), many=True)
        
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
                #is month??
                if is_month:
                    result_info = response.json()
                    print(f'result_info : {result_info}')
                    print(result_info['month_id'])
                    dog_info_id = result_info['month_id']
                    self.save_dog_token(user, dogs, dog_info_id, is_month)
                    print('token saved')
                    print('end')
                    request.session['month_id'] = dog_info_id
                    # get month result
                    response_month = self.get_result_month(dog_info_id)
                    print(response_month)
                    # get daily instance result
                    db_month = Monthly_Food.objects.filter(month_id=dog_info_id).values('food_1', 'food_2', 'food_3', 'food_4')
                    print(db_month)
                    first_record = db_month[0]
                    for idx in range(1, 5):
                        instance_dog_id = first_record[f'food_{idx}']
                        # get daily food
                        response_food = self.get_result_food(instance_dog_id)
                        # print('log response_food', response_food)
                        
                        response_nut7 = self.get_result_food_en(instance_dog_id)
                        # print('log response_nut7', response_nut7)

                        response_nut7 = self.get_result_nut7(instance_dog_id)
                        # print('log response_nut7', response_nut7)
                        
                        response_nut_report = self.get_result_nut_report(instance_dog_id)
                        # print('log response_nut_report', response_nut_report)
                        
                        response_nut_sufficient = self.get_result_nut_sufficient(instance_dog_id)
                        # print('log response_nut_sufficient', response_nut_sufficient)   
                    
                    return render(request, 'report/report_month.html')
                
                else:
                    result_info = response.json()
                    print(f'result_info : {result_info}')
                    print(result_info['dog_info_id'])
                    dog_info_id = result_info['dog_info_id']
                    self.save_dog_token(user, dogs, dog_info_id, is_month)
                    print('token saved')
                    print('end')
                    request.session['dog_info_id'] = dog_info_id
                    response_food = self.get_result_food(dog_info_id) 
                    # print('log response_food', response_food)

                    response_nut7 = self.get_result_nut7(dog_info_id)
                    # print('log response_nut7', response_nut7)
                    
                    response_nut7 = self.get_result_food_en(dog_info_id)
                        # print('log response_nut7', response_nut7)
                    
                    response_nut_report = self.get_result_nut_report(dog_info_id)
                    # print('log response_nut_report', response_nut_report)
                    
                    response_nut_sufficient = self.get_result_nut_sufficient(dog_info_id)
                    # print('log response_nut_sufficient', response_nut_sufficient)      

                    return render(request, 'report/report2.html')
            
            
        except requests.RequestException as e:
            # For network exceptions
            print("An error occurred:", str(e))
        return Response(status=400, data=dict(message="음식을 다시 설정하시요."))
