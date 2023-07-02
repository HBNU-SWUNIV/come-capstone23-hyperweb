from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view 

from .models import Dog_Info, Food_Result, Nut_7_save, Nut_report

from .serializers import DogInfoSerializer, FoodItemSerializer, Nut7Serializer, NutReportSerializer

from .calcurate import DietOptimizer
from itertools import zip_longest
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
        print('create food start')
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
        # print(input_list)

        calculated_recipe, nutrients_result = diet_optimizer.calculate_recipe(input_list, min_caloric_val)
        
        if calculated_recipe == 0 and nutrients_result == 0:
            return Response({'message': 'The solver could not solve the problem.'}, status=205)
        max_cal = diet_optimizer.max_calcurate(min_caloric_val + 50)
        min_cal = diet_optimizer.min_calcurate(min_caloric_val + 50)

        suffient = 0
        report_index = []
        report_percent = []
        report_actual = []
        report_minimun = []
        ranges = [(0, 7), (13, 14), (15, 29), (30, 34), (36, 39), (39, 42), (43, 47), 
                (49, 50), (60, 63), (82, 84), (85, 86), (123, 127), (131, 132)]

        for i, (nutrient, maximum, mininum) in enumerate(zip_longest(nutrients_result, max_cal, min_cal)):
            if nutrient == None:
                break
            if nutrient >= maximum:
                suffient += 1
            if any(start <= i < end for start, end in ranges):
                range_val = maximum - mininum
                if range_val == 0:
                    percent = 0
                    if nutrient > 0:
                        percent = 1
                else:
                    percent = round(((nutrient - mininum) / range_val), 3)
                if percent < 0:
                    percent = 0
                elif percent > 1:
                    percent = 1
                percent = percent * 100
                report_index.append(i)
                report_minimun.append(min_cal[i])
                report_percent.append(percent)
                report_actual.append(nutrient)
                
        #Dog info id load
        dog_info_id = Dog_Info.objects.latest('id').id
        dog_info_instance = Dog_Info.objects.get(id=dog_info_id)
        
        # 항목 저장 calculated_recipe
        for i in calculated_recipe:
            Food_Result.objects.create(
                dog_info = dog_info_instance,  # ForeignKey
                name = i[0],  # String
                unit = i[1],  # Float
            )

        #필수 7 요소 저장
        unit_df = ['A10100', 'A10200', 'A10300', 'A10400', 'A10500', 'A10600', 'A10700', 'A10701', 'A10702', 'A10703', 'A10704', 'A10705', 'A10706', 'A10800', 'A10801', 'A10802', 'B10100', 'B10200', 'B10300', 'B10400', 'B10500', 'B10600', 'B10700', 'B10800', 'B10900', 'B11000', 'B11100', 'B11200', 'C10100', 'C10102', 'C10103', 'C20100', 'C20200', 'C20300', 'C20301', 'C20302', 'C20303', 'C20500', 'C20600', 'C20601', 'C20700', 'C20900', 'C20901', 'C20902', 'C21200', 'C21300', 'C10200', 'C10201', 'C10202', 'C10300', 'C10301', 'C10302', 'C10303', 'C10304', 'C10305', 'C10306', 'C10307', 'C10308', 'C10400', 'C10401', 'C10402', 'D10100', 'D10200', 'D10201', 'D10202', 'D10203', 'D10204', 'D10205', 'D10206', 'D10207', 'D10208', 'D10209', 'D10210', 'D10301', 'D10302', 'D10303', 'D10304', 'D10305', 'D10306', 'D10307', 'D10308', 'D10309', 'E10100', 'E10200', 'E10300', 'E10400', 'E10401', 'E10402', 'E10403', 'E10404', 'E10405', 'E10406', 'E10407', 'E10408', 'E10409', 'E10410', 'E10411', 'E10412', 'E10413', 'E10414', 'E10415', 'E10416', 'E10615', 'E10500', 'E10502', 'E10503', 'E10504', 'E10505', 'E10506', 'E10507', 'E10508', 'E10509', 'E10600', 'E10601', 'E10602', 'E10603', 'E10605', 'E10606', 'E10607', 'E10609', 'E10610', 'E10611', 'E10612', 'E10614', 'E10700', 'E10800', 'E10900', 'E10901', 'E10902', 'E10903', 'Z10100', 'Z10300']
        nut_7_save_instace = Nut_7_save(
            dog_info=dog_info_instance,  # ForeignKey
            A10100=nutrients_result[0], 
            A10300=nutrients_result[2], 
            A10400=nutrients_result[3], 
            A10600=nutrients_result[5], 
            A10700=nutrients_result[6], 
            suffient=suffient, 
            lack = 132 - suffient
        )
        nut_7_save_instace.save()

        # Reporter 값 저장.
        for i, (a, b, c) in enumerate(zip_longest(report_actual, report_percent,report_minimun)):
            Nut_report.objects.create(
                dog_info=dog_info_instance,  # ForeignKey
                nut_name=f'{unit_df[report_index[i]]}',  # String
                actual_num = a,  # Float
                percent = b,  # Float
                min_num = c  # Float
            )
               
        result = {'dog_info_id': dog_info_id}
        print('create food end')
        return Response(result, status=status.HTTP_201_CREATED)
    
# @api_view(['POST'])
# def ResultFoodViewset(request):
#     serializer_Food = GetIdSerializer
    
        
#     return Response({"message": "Got some data!", "data": request.data})
# response food result
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
    
# class ResultFoodViewset(viewsets.ModelViewSet):
#     serializer_class = ResultFoodSerializer
#     def list(self, request, *args, **kwargs):
#         print('Retrieve dog info start')
        
#         # 요청으로부터 dog_info_id 가져오기
#         dog_info_id = request.GET.get('dog_info_id')
        
#         # Dog 정보 불러오기
#         food_result = Food_Result.objects.filter(dog_info_id=dog_info_id)
        
#         # Dog 정보 직렬화
#         food_serializer = DogInfoSerializer(food_result, many=True)
#         serialized_data = food_serializer.data
#         print(serialized_data)
        
#         return Response(serialized_data, status=status.HTTP_200_OK)
    
#     def retrieve(self, request, *args, **kwargs):
#         print('Retrieve dog info start')
        
#         # 요청으로부터 dog_info_id 가져오기
#         dog_info_id = request.GET.get('dog_info_id')
        
#         # Dog 정보 불러오기
#         food_result = Food_Result.objects.filter(dog_info_id=dog_info_id)
        
#         # Dog 정보 직렬화
#         food_serializer = DogInfoSerializer(food_result, many=True)
#         serialized_data = food_serializer.data
#         print(serialized_data)
        
#         return Response(serialized_data, status=status.HTTP_200_OK)
    

#식단을 안내해준다.s  mm