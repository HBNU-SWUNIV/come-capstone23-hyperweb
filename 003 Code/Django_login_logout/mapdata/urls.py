from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.member_reg, name='map'),
]