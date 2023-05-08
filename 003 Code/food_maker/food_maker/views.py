# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .calculate import DietOptimizer  # 해당 경로에 맞게 수정해주세요.


@csrf_exempt
def run_diet_optimizer(request):
    if request.method == 'POST':
        # JSON 입력을 받습니다.
        received_data = json.loads(request.body)

        # data_list를 추출합니다.
        data_list = received_data.get('data_list')

        # DietOptimizer 인스턴스를 생성하고 실행합니다.
        diet_optimizer = DietOptimizer(data_list)
        db_file = 'db2.sqlite3'
        conn = diet_optimizer.connect_db(db_file)
        input_list = diet_optimizer.get_input_list(conn, data_list)
        calculated_recipe, nutrients_result = diet_optimizer.calculate_recipe(input_list)

        # JSON 형식으로 결과를 반환합니다.
        response_data = {
            'calculated_recipe': calculated_recipe,
            'nutrients_result': nutrients_result
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method.'})



def javascript_test(request):
    return render(request, 'javascript_test.html')

