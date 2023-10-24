from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view 

from itertools import zip_longest
import time

from .models import Dog_Info, Monthly_Food, Food_Result, Nut_7_save, Nut_sufficient, Nut_report
from .serializers import DogInfoSerializer, MonthItemSerializer, FoodItemSerializer,Nut7Serializer, NutReportSerializer, NutSufficientSerializer
from .database import FoodSearch
from .daily_food import DietOptimizer
from .month_food import MenuGenerator


class DietHandler:
    def __init__(self, dog_mer, data_list, Food_db, dog_info_id=None):
        self.diet_optimizer = DietOptimizer(dog_mer, data_list, Food_db)
        self.dog_info = Dog_Info.objects.get(id=dog_info_id)
        # self.dog_info_instance = None
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
    # def get_dog_info_id(self, dog_info_id):
    #     self.dog_info_id = dog_info_id
        
    # def load_dog_info(self):
    #     # Dog info id load
    #     self.dog_info_id = Dog_Info.objects.latest('id').id
    #     self.dog_info_instance = Dog_Info.objects.get(id=self.dog_info_id)
    #     return self.dog_info_id
    
    def save_food_result(self):
        # 항목 저장 calculated_recipe
        for i in self.calculated_recipe:
            Food_Result.objects.create(
                dog_info=self.dog_info,  # ForeignKey
                name=i[0],  # String
                unit=i[1],  # Float
            )
        
    def save_nut_7(self):
        #필수 7 요소 저장
        suffient = self.diet_optimizer.get_nut_7()
            
        nut_7_save_instace = Nut_7_save(
            dog_info=self.dog_info,  # ForeignKey
            A10100=round(self.nutrients_result[0], 2), # 에너지 kcal
            A10300=round(self.nutrients_result[2], 2), # 단백질 
            A10400=round(self.nutrients_result[3], 2), # 지방
            A10600=round(self.nutrients_result[5], 2), # 탄수화물   
            A10700=round(self.nutrients_result[1], 2), # 수분량
            suffient=suffient, 
            lack = 39 - suffient
        )
        nut_7_save_instace.save()
        
    def save_nut_report(self):
        print(f'start nut report')
        # Reporter 값 저장.
        kr_unit_df = [
            "A10100", "A10200", "A10300", "A10400", "A10500", "A10600", "A10700", "A10800",
            "B10100", "B10200", "B10300", "B10400", "B10500", "B10600", "B10700", "B10800",
            "B10900", "B11000", "B11100", "B11200", "C10100", "C20100", "C20200", "C20300",
            "C20500", "C20600", "C20700", "C20900", "C21200", "C21300", "C10200", "C10300",
            "C10400", "D10100", "D10200", "E10100", "E10200", "E10400", "E10615", "E10700",
            "E10800", "E10900", "Z10300"
        ]
        unit_df = [
            "A10100", "A10200", "A10300", "A10400", "A10600",
            "B10100", "B10200", "B10300", "B10400", "B10500",
            "B10600", "B10700", "B10800", "B10900", "B11000",
            "B11200", "C10100", "C20100", "C20200", "C20300",
            "C20500", "C20601", "C20900", "C21200", "C10200",
            "C10300", "C10400", "D10201", "D10202", "D10203",
            "D10204", "D10205", "D10206", "D10207", "D10208",
            "D10209", "D10210", "E10601", "E10602"
        ]
        kr_nutrients = [
            "에너지", "수분", "단백질", "지방", "탄수화물", "칼슘", "철", "마그네슘", "인", "칼륨",
            "나트륨", "아연", "구리", "망간", "셀레늄", "요오드", "비타민 A", "티아민", "리보플라빈", "니아신",
            "판토텐산", "피리독신", "엽산_엽산당량", "비타민 B12", "비타민 D", "비타민 E", "비타민 K", "이소류신",
            "류신", "라이신", "메티오닌", "페닐알라닌", "트레오닌", "트립토판", "발린", "히스티딘", "아르기닌",
            "리놀레산", "알파 리놀렌산"
        ]
        
        report_index, report_minimum, report_percent, report_actual = self.diet_optimizer.process_nutrients()
        print('mid')
        for i, (a, b, c) in enumerate(zip_longest(report_actual, report_percent, report_minimum)):
            Nut_report.objects.create(
                dog_info=self.dog_info,  # ForeignKey
                nut_name=f'{unit_df[report_index[i]]}',  # String
                actual_num = a,  # Float
                percent = b,  # int
                min_num = round(c, 2)  # Float
            )
        # 필요조건 report_percent
        
        # 단백질 풍부한 식단 토큰 생성 0 2 !!
        if (report_actual[2] * 4 / report_actual[0]) >= 0.4:
            Nut_sufficient.objects.create(
                dog_info = self.dog_info,  # ForeignKey
                token_name = "A10300"
            )
            
        #  무기질 같은 경우 -> code 맨앞 B !! 6 ~ 15
        if (sum(report_actual[6:12]) > sum(report_minimum[6:12])):
            for num in range(6, 12):
                if report_percent[num] > 0:
                    Nut_sufficient.objects.create(
                        dog_info = self.dog_info,  # ForeignKey
                        token_name = f'{unit_df[num]}'
                    )
        
        # 비타민 A, D, E !!
        _vitamin_str = ['C10100', 'C10200', 'C10300']
        _vitamin_num = [16, 24, 25]
        if (sum(report_actual[i] for i in _vitamin_num) > sum(report_minimum[i] for i in _vitamin_num)):
            for num in _vitamin_num:
                if report_percent[num] > 0:
                    Nut_sufficient.objects.create(
                        dog_info = self.dog_info,  # ForeignKey
                        token_name = f'{unit_df[num]}'
                    )
        
        
        # 아미노산 군이 풍부한 식단  -> D  발린 히스티딘 아르기닌
        # 개별 토큰을 만들어주는 것이 아닌 아미노산 군에 대해 계산 
        # 발린
        if (sum(report_actual[34:37]) > sum(report_minimum[34:37])):
            for num in range(34, 37):
                if report_percent[num] > 0:
                    Nut_sufficient.objects.create(
                        dog_info = self.dog_info,  # ForeignKey
                        token_name = f'{unit_df[num]}'
                    )

    def macro_save(self):
        self.save_food_result()
        self.save_nut_report()
        self.save_nut_7()
        
class FoodViewSet(viewsets.ModelViewSet):
    queryset = Dog_Info.objects.all()
    serializer_class = DogInfoSerializer
    
    def __init__(self, *args, **kwargs):
        super(FoodViewSet, self).__init__(*args, **kwargs)
        self.dog_mer = None
    
    def create_dog_info(self):
        dog_info = Dog_Info(dog_mer=self.dog_mer)  # 예시 이름
        dog_info.save()
        return dog_info.id
    
    def create_month_food(self,dog_info_list):
        monthly_food = Monthly_Food()
        monthly_food.save()
        dog_infos = Dog_Info.objects.filter(id__in=dog_info_list)
        monthly_food.foods.add(*dog_infos)
        return monthly_food.id


    def create(self, request):
        Food_db = 'db2.sqlite3'
        
        print('create food start')
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        input_food = []
        for item in serializer.data:
            data = {'dog_mer': item['dog_mer'], 'food_items': item['food_items']}
            #추후에는 Dog id 를 갖고 와야함 현재는 dog_mer 로 instance의 개체를 찾기 때문임
            self.dog_mer = data['dog_mer']
            for food in data['food_items']:
                temp = [food['name'], food['unit']]
                input_food.append(temp)
        
        print('dog_mer', self.dog_mer)
        # Monthly food Generator
        if len(input_food) > 10:
            print('monthlyfood')
            searching_food = FoodSearch()
            searching_food.connect_db(Food_db)
            is_cat8 = searching_food.get_category_list(input_food)
            searching_food.close_db()
            print(is_cat8)
            # searching true
            true_indices = [index for index, value in enumerate(is_cat8) if value]
            # searing false
            false_indices = [index for index, value in enumerate(is_cat8) if not value]
            print(f'true {true_indices}')
            print(f'false {false_indices}')
            menu_gerator = MenuGenerator(true_indices, false_indices)
            monthly_food_list = menu_gerator.generate()
            dog_info_ids = []
            # dog_info_ids = [71, 72, 73, 74]
            
            for idx, menu_num in enumerate(monthly_food_list):
                input_food_sep = []
                for (idx, weight) in menu_num:
                    input_food_sep.append(input_food[idx])
                print(input_food_sep)
                # dog unique id generate
                dog_unique_id = self.create_dog_info()
                handler = DietHandler(self.dog_mer, input_food_sep, Food_db, dog_unique_id)
                if handler.calculate_recipe():
                    handler.macro_save()
                    dog_info_ids.append(dog_unique_id)
                    print('create food end')
                else:
                    return Response({'message': 'The solver could not solve the problem.'}, status=205)
            print(dog_info_ids)
            
            #test
            month_id_key = self.create_month_food(dog_info_ids)
            result = {'month_id': month_id_key}
            #test
            # result = {'month_id': 2}
            # print(8)
            return Response(result, status=status.HTTP_201_CREATED)
            
            
        else: # daily food generator
            # dog unique id generate
            dog_unique_id = self.create_dog_info()
            handler = DietHandler(self.dog_mer, input_food, Food_db, dog_unique_id)
            if handler.calculate_recipe():
                handler.macro_save()
                result = {'dog_info_id': dog_unique_id}
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
    month_id = input_data.get('month_id')
    print(month_id)
    
    # # Dog 정보 불러오기
    # month_result = Monthly_Food.objects.get(id=month_id)
    # month_serialized = MonthItemSerializer(month_result, many=True)
    
    # Dog 정보 불러오기
    monthly_food_instance = Monthly_Food.objects.get(id=month_id)
    dog_info_ids = monthly_food_instance.foods.values_list('id', flat=True)
    
    json_send = {
        'food_1':dog_info_ids[0],
        'food_2':dog_info_ids[1],
        'food_3':dog_info_ids[2],
        'food_4':dog_info_ids[3],
        'month_id':month_id
    }

    print('month_serialized', dog_info_ids)
    
    
    print('result month food info end')
    return Response(json_send)

@api_view(['POST'])
def result_food(request):
    print('result food info start')
    input_data = request.data
    print(f'input_data {input_data}')
    # 요청으로부터 dog_info_id 가져오기
    dog_info_id = input_data.get('dog_info_id')
    print(dog_info_id)
    
    # Dog 정보 불러오기
    food_result = Food_Result.objects.filter(dog_info_id=dog_info_id)
    food_serialized = FoodItemSerializer(food_result, many=True)
    
    print('result food info end')
    return Response(food_serialized.data)

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
    result_nut_sufficient_serialized = NutSufficientSerializer(result_nut_sufficient_result, many=True)
    print(result_nut_sufficient_result)
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
    