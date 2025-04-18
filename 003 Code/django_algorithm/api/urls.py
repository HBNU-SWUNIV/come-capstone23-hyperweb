from django.urls import include, path
from rest_framework import routers
from . import views #views.py import

router = routers.DefaultRouter() #DefaultRouter를 설정
# router.register('Item', views.ItemViewSet) #itemviewset 과 item이라는 router 등록

# urlpatterns = [
#     path('', include(router.urls))
# ]

router.register('Food_Item', views.FoodViewSet, basename='Food_Item') #FoodViewSet를 Food_Item router로 등록

urlpatterns = [
    path('', include(router.urls)),
    path('result_month/', views.result_month, name='result_month'),
    path('result_food/', views.result_food, name='result_food'),
    path('result_food_en/', views.result_food_en, name='result_food_en'),
    path('result_nut7/', views.result_nut7, name='result_nut7'),
    path('result_nut_sufficient/', views.result_nut_sufficient, name='result_nut_sufficient'),
    path('result_nut_report/', views.result_nut_report, name='result_nut_report')
]