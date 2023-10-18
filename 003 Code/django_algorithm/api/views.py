from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view 

from itertools import zip_longest
import time

from .models import Dog_Info, Monthly_Food, Food_Result, Nut_some_save, Nut_7_save, Nut_sufficient, Nut_report
from .serializers import DogInfoSerializer, MonthItemSerializer, FoodItemSerializer, NutSomeSerializer,Nut7Serializer, NutReportSerializer
from .database import FoodSearch
from .daily_food import DietOptimizer
from .month_food import MenuGenerator


class DietHandler:
    def __init__(self, dog_mer, data_list, Food_db, dog_info=None):
        self.diet_optimizer = DietOptimizer(dog_mer, data_list, Food_db)
        self.dog_info_id = dog_info
        self.dog_info_instance = None
        self.calculated_recipe = None
        self.nutrients_result = None
        
    def calculate_recipe(self):
        # step1 calculate start
        self.calculated_recipe = self.diet_optimizer.step1()
        self.nutrients_result = self.diet_optimizer.nut_report()
        if self.calculated_recipe == 0 or self.nutrients_result == 0:
            # Return some error indication if necessary
            return False
        return True

    # DB transaction error appear !!  self.dog_info_instance not need
    def load_dog_info(self):
        # Dog info id load
        self.dog_info_id = Dog_Info.objects.latest('id').id
        self.dog_info_instance = Dog_Info.objects.get(id=self.dog_info_id)
        return self.dog_info_id
    
    def save_food_result(self):
        # 항목 저장 calculated_recipe
        for i in self.calculated_recipe:
            Food_Result.objects.create(
                dog_info=self.dog_info_instance,  # ForeignKey
                name=i[0],  # String
                unit=i[1],  # Float
            )
            
    def save_nut_some(self):
        nut_some_save_instace = Nut_some_save(
            dog_info=self.dog_info_instance,  # ForeignKey
            B10100=round(self.nutrients_result[0], 2), 
            B10300=round(self.nutrients_result[2], 2), 
            B10700=round(self.nutrients_result[3], 2),
        )
        nut_some_save_instace.save()
        
    def save_nut_7(self):
        #필수 7 요소 저장
        suffient = self.diet_optimizer.get_nut_7()
            
        nut_7_save_instace = Nut_7_save(
            dog_info=self.dog_info_instance,  # ForeignKey
            A10100=round(self.nutrients_result[0], 2), 
            A10300=round(self.nutrients_result[2], 2), 
            A10400=round(self.nutrients_result[3], 2),  
            A10600=round(self.nutrients_result[5], 2),  
            A10700=round(self.nutrients_result[6], 2),  
            suffient=suffient, 
            lack = 132 - suffient
        )
        nut_7_save_instace.save()
        
    def save_nut_report(self):
        # Reporter 값 저장.
        unit_df = [
            "A10100", "A10200", "A10300", "A10400", "A10500", "A10600", "A10700", "A10800",
            "B10100", "B10200", "B10300", "B10400", "B10500", "B10600", "B10700", "B10800",
            "B10900", "B11000", "B11100", "B11200", "C10100", "C20100", "C20200", "C20300",
            "C20500", "C20600", "C20700", "C20900", "C21200", "C21300", "C10200", "C10300",
            "C10400", "D10100", "D10200", "E10100", "E10200", "E10400", "E10615", "E10700",
            "E10800", "E10900", "Z10300"
        ]
        
        report_index, report_minimum, report_percent, report_actual = self.diet_optimizer.process_nutrients()
        print('mid')
        for i, (a, b, c) in enumerate(zip_longest(report_actual, report_percent, report_minimum)):
            Nut_report.objects.create(
                dog_info=self.dog_info_instance,  # ForeignKey
                nut_name=f'{unit_df[report_index[i]]}',  # String
                actual_num = a,  # Float
                percent = b,  # Float
                min_num = round(c, 2)  # Float
            )
        # 필요조건 report_percent
        
        # 단백질 풍부한 식단 토큰 생성 0 2
        if (report_actual[2] * 4 / report_actual[0]) >= 0.4:
            Nut_sufficient.objects.create(
                dog_info = self.dog_info_instance,  # ForeignKey
                token_name = "단백질이_풍부한_식단"
            )
            
        # # 무기질 풍부한 식단 토큰 생성 [8:21]
        # b_class_columns = [
        #     "칼슘", "철", "마그네슘", "인", "칼륨", "나트륨",
        #     "아연", "구리", "망간", "셀레늄", "몰리브덴", "요오드",
        # ]
        # if (sum(report_actual[8:20]) > sum(report_minimum[8:20])):
        #     for num in range(8, 20):
        #         if report_percent[num] > 0:
        #             Nut_sufficient.objects.create(
        #                 dog_info = self.dog_info_instance,  # ForeignKey
        #                 token_name = f'{b_class_columns[num]}이(가)_풍부한_식단'
        #             )
        
        # 비타민 D, A, E 풍부한 식단 토큰 생성 46 28 49
        _vitamin_str = ['비타민 A', '비타민 D', '비타민 E']
        _vitamin_num = [20, 30, 31]
        if (sum(report_actual[i] for i in _vitamin_num) > sum(report_minimum[i] for i in _vitamin_num)):
            for num in _vitamin_num:
                if report_percent[num] > 0:
                    Nut_sufficient.objects.create(
                        dog_info = self.dog_info_instance,  # ForeignKey
                        token_name = f'{_vitamin_str}이(가)_풍부한_식단'
                    )
        
        # # 비타민 B 풍부한 식단 토큰 생성 [21:30]
        # b_class_columns = [
        #     "티아민", "리보플라빈", "니아신", "판토텐산", "비타민 B6", "비오틴",
        #     "엽산_엽산당량", "비타민 B12", "비타민 C",
        # ]
        # if (sum(report_actual[21:33]) > sum(report_minimum[21:33])):
        #     for num in range(21, 33):
        #         if report_percent[num] > 0:
        #             Nut_sufficient.objects.create(
        #                 dog_info = self.dog_info_instance,  # ForeignKey
        #                 token_name = f'{b_class_columns[num]}이(가)_풍부한_식단'
        #             )
        
        # # 아미노산 풍부한 식단 토큰 생성 [33:36]
        # b_class_columns = ["총 아미노산", "총 필수아미노산", "콜레스테롤"]
        # if (sum(report_actual[33:36]) > sum(report_minimum[33:36])):
        #     for num in range(33, 36):
        #         if report_percent[num] > 0:
        #             Nut_sufficient.objects.create(
        #                 dog_info = self.dog_info_instance,  # ForeignKey
        #                 token_name = f'{b_class_columns[num]}이(가)_풍부한_식단'
        #             )

    def macro_save(self):
        self.save_food_result()
        self.save_nut_7()
        self.save_nut_some()
        self.save_nut_report()
        
class FoodViewSet(viewsets.ModelViewSet):
    queryset = Dog_Info.objects.all()
    serializer_class = DogInfoSerializer
    
    def create_dog_info(self, mer):
        dog_info = Dog_Info(dog_mer=mer)  # 예시 이름
        dog_info.save()
    # dog_info_id = Dog_Info.objects.latest('id').id
    
    def create_month_food(self, month_data):
        Monthly_Food.objects.create(
            food_1 = month_data[0],
            food_2 = month_data[1],
            food_3 = month_data[2],
            food_4 = month_data[3]
        )

    def create(self, request):
        Food_db = 'db2.sqlite3'
        
        print('create food start')
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data_list = []
        for item in serializer.data:
            data = {'dog_mer': item['dog_mer'], 'food_items': item['food_items']}
            dog_mer = data['dog_mer']
            for food in data['food_items']:
                temp = [food['name'], food['unit']]
                data_list.append(temp)
        
        print('dog_mer', dog_mer)
        # Monthly food Generator
        if len(data_list) > 10:
            print('monthlyfood')
            searching_food = FoodSearch()
            searching_food.connect_db(Food_db)
            is_cat8 = searching_food.get_category_list(data_list)
            searching_food.close_db()
            print(is_cat8)
            # searching true
            true_indices = [index for index, value in enumerate(is_cat8) if value]
            # searing false
            false_indices = [index for index, value in enumerate(is_cat8) if not value]
            
            menu_gerator = MenuGenerator(true_indices, false_indices)
            monthly_food_list = menu_gerator.generate()
            dog_info_ids = []
            # temp = DietHandler(dog_mer, menu, Food_db)
            # loc_dog_info, loc_dog = temp.load_dog_info()
            for idx, menu_num in enumerate(monthly_food_list):
                menu = []
                for (idx, weight) in menu_num:
                    menu.append(data_list[idx])
                print(menu)
                handler = DietHandler(dog_mer, menu, Food_db)
                self.create_dog_info(dog_mer)
                dog_info = handler.load_dog_info()
                if handler.calculate_recipe():
                    handler.macro_save()
                    dog_info_ids.append(dog_info)
                    print('create food end')
                else:
                    return Response({'message': 'The solver could not solve the problem.'}, status=205)
            print(dog_info_ids)
            self.create_month_food(dog_info_ids)
            month_id = Monthly_Food.objects.latest('id').id
            result = {'month_id': month_id}
            print(dog_info_ids)
            return Response(result, status=status.HTTP_201_CREATED)
            
            
        else: # daily food generator
            handler = DietHandler(dog_mer, data_list, Food_db)
            dog_info = handler.load_dog_info()
            if handler.calculate_recipe():
                handler.macro_save()
                result = {'dog_info_id': dog_info}
                print('create food end')
                
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                print('error')
                return Response({'message': 'The solver could not solve the problem.'}, status=205)
            

@api_view(['POST'])
def result_month(request):
    print('result month food info start')
    input_data = request.data
    
    # 요청으로부터 dog_info_id 가져오기
    dog_info_id = input_data.get('dog_info_id')
    print(dog_info_id)
    
    # Dog 정보 불러오기
    month_result = Monthly_Food.objects.filter(dog_info_id=dog_info_id)
    month_serialized = MonthItemSerializer(month_result, many=True)
    
    print('result month food info end')
    return Response(month_serialized.data)

@api_view(['POST'])
def result_food(request):
    print('result food info start')
    input_data = request.data
    
    # 요청으로부터 dog_info_id 가져오기
    dog_info_id = input_data.get('dog_info_id')
    print(dog_info_id)
    
    # Dog 정보 불러오기
    food_result = Food_Result.objects.filter(dog_info_id=dog_info_id)
    food_serialized = FoodItemSerializer(food_result, many=True)
    
    print('result food info end')
    return Response(food_serialized.data)

# response food some nut 
@api_view(['POST'])
def result_nutsome(request):
    print('result food some nut  info start')
    input_data = request.data
    
    # 요청으로부터 dog_info_id 가져오기
    dog_info_id = input_data.get('dog_info_id')
    print(dog_info_id)
    
    # Dog 정보 불러오기
    month_result = Nut_some_save.objects.filter(dog_info_id=dog_info_id)
    month_serialized = NutSomeSerializer(month_result, many=True)
    
    print('result month food info end')
    return Response(month_serialized.data)

# response food nut 7
@api_view(['POST'])
def result_nut7(request):
    print('7_nut info start')
    input_data = request.data
    
    # 요청으로부터 dog_info_id 가져오기
    dog_info_id = input_data.get('dog_info_id')
    print(dog_info_id)
    
    # Dog 정보 불러오기
    nut_result = Nut_7_save.objects.get(dog_info_id=dog_info_id)
    nut_serialized = Nut7Serializer(nut_result)
    
    print('7_nut info end')
    return Response(nut_serialized.data)

# response food nut report
@api_view(['POST'])
def result_nut_sufficient(request):
    print('result nut_sufficient info start')
    input_data = request.data
    
    # 요청으로부터 dog_info_id 가져오기
    dog_info_id = input_data.get('dog_info_id')
    print(dog_info_id)
    
    # Dog 정보 불러오기
    result_nut_sufficient_result = Nut_sufficient.objects.filter(dog_info_id=dog_info_id)
    result_nut_sufficient_serialized = NutReportSerializer(result_nut_sufficient_result, many=True)
    
    print('result nut_sufficient info end')
    return Response(result_nut_sufficient_serialized.data)

# response food nut report
@api_view(['POST'])
def result_nut_report(request):
    print('result food info start')
    input_data = request.data
    
    # 요청으로부터 dog_info_id 가져오기
    dog_info_id = input_data.get('dog_info_id')
    print(dog_info_id)
    
    # Dog 정보 불러오기
    nut_report_result = Nut_report.objects.filter(dog_info_id=dog_info_id)
    nut_report_serialized = NutReportSerializer(nut_report_result, many=True)
    
    print('result food info end')
    return Response(nut_report_serialized.data)
    