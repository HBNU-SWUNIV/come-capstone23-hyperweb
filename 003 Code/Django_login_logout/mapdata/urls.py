from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('map/', views.map, name='map'),
    path('map/<int:n>', views.map_list, name='map'),
]

