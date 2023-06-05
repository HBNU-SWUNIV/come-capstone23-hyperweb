from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index),
    path('save_image/', views.save_image, name='save_image'),
]