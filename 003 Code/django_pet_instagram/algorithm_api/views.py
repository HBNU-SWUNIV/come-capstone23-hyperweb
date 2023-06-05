from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Food, FoodList
from user.models import User
from user.models import Dog 
from django.forms.models import model_to_dict
import requests
import json


def caloric_generator(age, weight, activate, bcs, sex):
    cal_weight = 1
    # weight = 15

    MER = 132 * (weight ** 0.75)

    #input
    # activate = 2
    # sex = 0
    # age = 0
    # bcs = 4

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

    def get(self, request):
        # login session 개선 필요
        if isinstance(request.user, ModelBackend) and request.user.is_authenticated:
            # 로그인된 사용자인 경우
            user = request.user
            dogs = Dog.objects.filter(user=user.id)
            print(dogs.age, dogs.weight, dogs.activate, dogs.bcs, dogs.sex)
            self.dog_mer = caloric_generator(dogs.age, dogs.weight, dogs.activate, dogs.bcs, dogs.sex)
        else:
            print('not login')
        return render(request, "algorithm_api/Food_view.html")
    
    def post(self, request):
        self.dog_mer = caloric_generator(self.age, self.weight, self.activate, self.bcs, self.sex)

        print('post start ')
        body_unicode = request.body.decode('utf-8')  # Decode the request body
        body_data = json.loads(body_unicode)  # Parse it into Python dictionary
        input_result = body_data.get('foods')  # Get the foods data

        if not input_result:
            print('Invalid request data')
            return HttpResponseBadRequest("Invalid request data")

        food_list_model = FoodList()
        food_list_model.save()
        food_dicts = []
        for food_data in input_result:
            food_name = food_data['food']
            food_weight = food_data['weight']  # If you need to use the weight
    
            food_dict = {
                "name": food_name,
                "unit": food_weight  # You can add more fields as necessary
            }
            food_dicts.append(food_dict)

        print(food_dicts)
        dog_mer = self.dog_mer
        json_dict = {
            "dog_mer" : dog_mer,
            "food_items": food_dicts
        }
        json_list = [json_dict]
        print(json_list)

        response = requests.post("http://127.0.0.1:6000/Food_Item/", json=json_list)
        if response.status_code == 200:
            # If successful, send a GET request to the same server
            get_response = requests.get("http://127.0.0.1:6000/Food_Item/")
            
            # Process the GET response
            if get_response.status_code == 200:
                get_data = get_response.json()
                # Do something with the data...
            else:
                print("GET request failed with status code:", get_response.status_code)
        else:
            print("POST request failed with status code:", response.status_code)
        print(get_data)

        return render(request, "algorithm_api/Food_view.html")


# def food_view(request):
#     if request.method == 'POST':

#         food_names = request.POST.getlist('foods')
#         food_list = FoodList()
#         food_list.save()

#         for food_name in food_names:
#             food, created = Food.objects.get_or_create(name=food_name)
#             food_list.foods.add(food)

#         return HttpResponseRedirect('/')

#     return render(request, 'algorithm_api/new_input.html')
